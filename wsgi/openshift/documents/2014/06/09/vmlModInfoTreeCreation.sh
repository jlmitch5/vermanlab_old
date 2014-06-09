#!/bin/sh

# TODO: May be better to name the MACHINE_NAME something
# more useful...perhaps which version of the kernel the
# machine is actually running?
# --
# MACHINE_NAME is the host name of the machine, as well as the
# root level of the prettified modinfo package
MACHINE_NAME=$(hostname)

# TODO: As of this version, the script deletes the folder if it
# has been found before...these meen the script cannot be
# "reused" after it has been used once.  Is this going to be
# an impediment?
# --
# create (or move into) a folder for the specific machine, designated by hostname
# check to see if the root folder exists
if [ -a "$MACHINE_NAME" ]
then
	# if root folder exists, delete/create/cd into it
	rm -rf "$MACHINE_NAME"
	mkdir "$MACHINE_NAME"
	cd "$MACHINE_NAME"
else
	# if root folder doesn't exist, create it and cd into it
	mkdir "$MACHINE_NAME"
	cd "$MACHINE_NAME"
fi

# create (or move into) a folder for each kernel version, designated by kernel version
for filename in /lib/modules/*; do
	# kernel_version: cut the kernel version off the rest of the file path
	kernel_version=$(echo $filename | awk -F / '{print $4}')
	# create and move into the file
	mkdir "$kernel_version"
	cd "$kernel_version"
	# kernel_version_path: full path for kernel_version
	# this is how we get to the kernel's dir in our package (2nd to root)
	kernel_version_path=$(pwd)

	# go ahead and make the pci and usb sub-directories
	mkdir "$kernel_version_path/pci"
	# mkdir "$kernel_version_path/usb"

	# move into the actual kernel path
	cd "$filename"

	# iterate through all kernel modules
	find -name *\.ko | while read line; do
		# TODO: the work in this while loop is where all real "parsing is done"
		# it should work (on all edge-cases that I could think of), but it's
		# probably inefficient.  It will be necessary to make this better 
		# in the future if this will need to run on more machines that
		# just once per kernel version
		# --
		# module_name: prettified version of the module name
		# for use with modinfo
		module_name_not_pretty=$(basename "$line")
		module_name=${module_name_not_pretty%%.*}

		# modinfo_params: the parameters used for running mod info
		modinfo_params="-k $kernel_version $module_name"

		# module_name_path: create a directory in our output tree based on the module_name
		module_name_path="$kernel_version_path/$module_name"
		# create the dir for the module name
		mkdir "$module_name_path"

		# raw_modinfo_file: create the file which will hold 
		# raw modinfo in the module_name_path dir
		raw_modinfo_file="$module_name_path/raw_modinfo_output"
		touch "$raw_modinfo_file"

		# pipe (not append) the modinfo into the modinfo file
		modinfo $modinfo_params 1> $( echo "$raw_modinfo_file" )

		# remove the module_name_path dir if modinfo returned nothing
		if [ ! -s "$raw_modinfo_file" ]
		then
			rm -f "$module_name_path"
		else
			# you have a module with some relevant modinfo stuff said about it
			# parse
			# driver_type: see if the driver_type is pci of usb
			driver_type=$(awk '/alias:/' $raw_modinfo_file | awk '{print $2}' \
 			| awk -F : '{print $1}' )
 			if [[ $driver_type == *pci* ]]
    			then
       				# move the module_name dir into the pci dir
        			moved_module_name_path="$kernel_version_path/pci/$module_name"
        			mv $module_name_path $moved_module_name_path
        			# remove the old module
        			rm -rf $module_name_path

			# note, don't support usb just yet
			# wait until we hear back from the usb kernel dev
    			# elif [[ $driver_type == *usb* ]]
    			# then
        			# move the module_name dir into the usb dir
        			# moved_module_name_path="$kernel_version_path/usb/$module_name"
        			# mv $module_name_path $moved_module_name_path
        			# remove the old module
        			# rm -rf $module_name_path
			else
				moved_module_name_path="DOESN'T_EXIST"
				# module not pci or usb, delete it
				rm -rf $module_name_path
			fi

			# if moved_module_name_path exists (was usb/pci), start parsing
			if [ -d "$moved_module_name_path" ]
			then
				# create files and path vars for aliases, srcversion, and 
				# version (for each module)
				aliases="$moved_module_name_path/aliases"
				srcversion="$moved_module_name_path/srcversion"
				version="$moved_module_name_path/version"
				touch "$aliases"
				touch "$srcversion"
				touch "$version"

				# update the raw_modinfo_file_reference
				moved_raw_modinfo_file="$moved_module_name_path/raw_modinfo_output"


				# aliases input (pull aliases from moved_raw_modinfo_file)
				if [[ $(awk '/alias:/' $moved_raw_modinfo_file | awk '{print $2}' ) == pci:* ]]
				then
					# cut off all extraneous values
					awk '/alias:/' "$moved_raw_modinfo_file" | awk \
					'{print $2}' | awk -F : '{print $2}' | awk -F "bc" \
					'{print $1}' | sed 's/\*//' | sed 's/0000//' | sed 's/sd/:/' | \
					sed 's/\*//' | sed 's/sv/:/' | sed 's/\*//' | sed 's/0000//' | \
					sed 's/d/:/' | sed 's/\*//' | \
					sed 's/v//' | sed 's/0000//' | sed 's/\*//' | sed 's/0000//' \
					>> $aliases
				fi

				# srcversion input (pull srcversion from moved_raw_modinfo_file)
				if [[ $(cat $moved_raw_modinfo_file | awk '{print $1}' ) \
				== *srcversion:* ]]
				then
					awk '/srcversion:/' "$moved_raw_modinfo_file" | \
					awk '{print $2}' >> $srcversion
				else
					rm -rf "$srcversion"
				fi

				# version input
				# driver_version_value: is the driver version of the module 
				# (if it exists)
				driver_version_value=$(awk '$1=="version:" {print $2}' \
				$moved_raw_modinfo_file )
				if [ ! -z "$driver_version_value" ]
				then
					echo $driver_version_value >> "$version"
				else
					rm -rf "$version"
				fi

				# remove the raw_modinfo_file (it's no longer useful)
				rm -rf "$moved_raw_modinfo_file"

				# finished with this module
				# iterate through the next module
			fi	
		fi
	done

	# move back to the machine directory so you can put the
	# next kernel version where it goes in our package
	cd "$kernel_version_path"
	cd ..
done
