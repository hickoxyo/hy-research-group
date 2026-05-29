#! /usr/bin/bash
# JERID MCDONALD
# HICKOX-YOUNG ENERGY MATERIALS RESEARCH GROUP
# VASP ENCUT AND KPOINT CONVERGENCE TESTING, W/ FILE POPULATION
#--------------------------------------------------------------
#"MAKE SURE YOU HAVE A FOLDER TITLED initial_files containing:"
#"POSCAR.backup POTCAR.backup INCAR.backup AND KPOINTS.backup"
#--------------------------------------------------------------
# MAKE SURE THE VARIABLES IN THE INCAR.backup AND KPOINT.backup FILES  ARE RENAMED TO:
# "REPLACED-ENCUT-VALUE" & "REPLACED-NxNxN-KPOINT-DENSITY"
#-----------------------------------------------------------------

#TO DO									
#LABEL HOW THE *.backup FILES ARE MODIFIED <-- for others to use

#For automating vasp processes with multiple cores
#RUN VASP WITH &
#RECORD THE PID IN A VARIABLE WITH THE PROCESSOR CORE NAMES (core1-2_process)
#NOTE WHICH PROCESSORS ITS ASSIGNED TO
#-REPEAT
#NAVIGATE TO THE NEXT FOLDER
#ASSUME FILES ARE ALREADY NAMED PROPERLY AND IN PLACE
#RUN VASP WITH &, TWO PROCESSOR CORES AWAY FROM THE LAST ONE
#-DO THIS A MAX OF FIVE TIMES
#-WHEN ONE PROCESS IS FREED (CHECK WITH kill 0) START THE NEXT PROCESS ON ITS CORE



#FUNCTIONS
#===========================
# encut convergence function
#===========================
encutConvergence () {
 # ensure that the user's value are reasonable relative to each other (beginning is not greater than the end, step size is not larger than the entire range)
 # verify user input
 while true;
 do
  # get ENCUT range from user
  echo "What is the low end of your ENCUT range?"
  read encutMIN
  echo "What is the high end of your ENCUT range?"
  read encutMAX
  # verify the values make sense
  if [[ "$encutMIN" -le "$encutMAX" ]];
  then    
   break # free user from first loop
  else
   echo "Your range didn't make sense. Please try entering them again."
  fi  
 done
 # getENCUT step size from user
 while true;
 do
  echo "What is your ENCUT step size?"
  read encutSTEP
  if [[ "$encutSTEP" -le $(($encutMAX - $encutMIN)) ]];
  then
   break  # free user from second loop
  else 
   echo "Your range step-size didn't make sense. Please try entering it again."
  fi
 done
 # get kpoint mesh density. no need to verify. user, beware of hubris
 echo "What is your NxNxN KPOINT mesh density?"
 echo "Enter one number: "
 read kpoints
 
 #make a file for every step of the ENCUT range being checked, and populate it with POTCAR, POSCAR, INCAR, and KPOINT files
 for ((i = $encutMIN ; i <= $encutMAX ; i += $encutSTEP));
 do
  if [[ $encutSTEP -eq 0 ]]
   then encutSTEP=1
  fi

  cp -r  initial_files/ "$i"/
  #navigate to the new folder
  cd $i
  # rename backup files to prep for use
  cp "INCAR.backup" INCAR
  cp "KPOINTS.backup" KPOINTS
  cp "POTCAR.backup" POTCAR
  cp "POSCAR.backup" POSCAR
  # replace ENCUT value (line 41, INCAR)
  sed -i "s/REPLACED-ENCUT-VALUE/$i/g" INCAR
  # replace KPOINT value (line 4, KPOINTS)
  sed -i "s/REPLACED-NxNxN-KPOINT-DENSITY/$kpoints $kpoints $kpoints/g" KPOINTS
  
  # increase this by two for every new process you want to run
  #TODO: PROMPT USER FOR WHAT CORES THEY WANT TO RUN ON		
  #mpirun -n 2 --bind-to core --cpu-set 0,1 vasp_std |& tee -a terminal_output.txt
  mpirun -n 2 vasp_std |& tee -a terminal_output.txt

  # store the final e0 value, the ENCUT level, and the KPOINT mesh density
  export final_e0=$(grep e_0_energy vasprun.xml | tail -1 | cut -c 29-40)
  export encut_value=$(grep ENCUT vasprun.xml | head -1 | cut -c 22-25)
  export kpoint_value=$(grep "! dimensions" KPOINTS | tail -1 | cut -c 1-2)
  # export stored values to text file for formatting
  echo -n "$final_e0" >>../results.txt
  echo -n "$encut_value " >>../results.txt
  echo -n "$kpoint_value" >>../results.txt
  echo >>../results.txt # new line
  # inform the user of what's being printed
  echo "This is what I read"
  echo "Final E0: $final_e0"
  echo "Encut: $encut_value"
  echo "KPOINT value: $kpoint_value"
  # go back up one directory
  cd ..
 done
 # export the text file to a spreadsheet
 sed 's/ /;/g' results.txt >>results.csv
}



# ===========================
# kpoint convergence function
# ===========================
kpointConvergence () {
 while true; do
  #get input from user
  echo "What is the low end of your KPOINT range?"
  read kpointMIN
  echo "What is the high end of your KPOINT range?"
  read kpointMAX
  if [[ "$kpointMIN" -le "$kpointMAX" ]];
  then
   break
  else 
   echo "Your KPOINT range doesn't make sense. Please enter new values."
  fi
 done
 # no need to verify these values. user hubris beware
 echo "What ENCUT value would you like to use?"
 read encutValue

 #START CORE ASSIGNMENT LOOP			
 # iterate through the user's range
 for ((i = $kpointMIN ; i <= $kpointMAX;));
 do 
  # create and navigate to new directory
  cp -r -v initial_files/ $i/
  cd $i
  # rename backup files and prep for use
  mv INCAR.backup INCAR
  mv KPOINTS.backup KPOINTS
  mv POSCAR.backup POSCAR
  mv POTCAR.backup POTCAR
  # replace ENCUT value (line 41, INCAR)
  sed -i "s/REPLACED-ENCUT-VALUE/$encutValue/g" INCAR
  # replace KPOINT value (line 4, KPOINTS)
  #sed -i '4s/*/$n $n $n ! dimensions/g KPOINTS
  sed -i "s/REPLACED-NxNxN-KPOINT-DENSITY/$i $i $i/" KPOINTS

  #RUN KPOINT TESTING
  #mpirun -n 2 --bind-to core --cpu-set 0,1 vasp_std |& tee -a terminal_output.txt
  mpirun -n 2 vasp_std |& tee -a terminal_output.txt
  
  # store results
  export final_e0=$(grep e_0_energy vasprun.xml | tail -1 | cut -c 29-40)
  export encut_value=$(grep ENCUT vasprun.xml | head -1 | cut -c 22-25)
  export kpoint_value=$(grep "! dimensions" KPOINTS | tail -1 | cut -c 1-2)
  # export results
  echo -n "$final_e0" >>../results.txt
  echo -n "$encut_value" >> ../results.txt
  echo -n "$kpoint_value" >> ../results.txt
  echo >>../results.txt # new line
  # move back out of the directory
  cd ..
  # export to csv
  sed 's/ /;/g' results.txt >>results.csv

  # properly increment kpoint value
  # check if value is less than 8 and even
  if [[ ($i -lt 8 ) && ($(($i % 2)) == 0) ]];
  then
   i=$((i+2))
  # check if value is less than 8 and odd
  elif [[ ($i -lt 8) && ($(($i % 2)) == 1) ]];
  then
   i=$((i-1))
  # check if value is 8
  elif [[ ($i == 8) ]];
  then
   i=$((i+1))
  # check if value is greater than 8 and even
  elif [[ ($i -gt 8 ) && ($(($i % 2)) == 0) ]];
  then
   i=$((i-1))
  # check if value is greater than 8 and odd
  elif [[ ($i -gt 8) && ($(($i % 2)) == 1) ]];
  then
   i=$((i+2))
  else
   echo "Kpoint value error"
  fi
 done
}


#=======================================
#==========
# MAIN BODY
#==========
# checks for existing files
for file_name in POTCAR POSCAR INCAR KPOINTS;
do
 if [ ! -e initial_files/$file_name.backup ]; then
 echo "ERROR: File $file_name not found"
 echo "Make sure you have a directory labeled 'initial_files' that contains POTCAR, POSCAR.backup, INCAR.backup, and KPOINTS.backup files."
 exit 1
 fi
done

# prompt user for cleanup
erase_files=false
echo "Would you like to delete any old files? "
ls
echo "[WARNING] THIS WILL DELETE ALL NON-TEST FILES IN THE CURRENT DIRECTORY [WARNING]"
read -p "Type 'Y' or 'N': " loop_answer
echo # new line to separate prompts
case $loop_answer in
 [Yy]* ) erase_files=true;;
 [Nn]* ) erase_files=false;;
esac

# erase old files if prompted
if $erase_files; then
 # remove all directories except for 'initial_files'
 find . -mindepth 1 -type d ! -name 'initial_files' -exec rm -r {} +
 # make backup of old results to be safe
 cp results.txt old_results.txt && cp results.csv old_results.csv
 find . -mindepth 1 -maxdepth 1 -type f -name 'results.*' -exec rm {} +
 ls
 echo "Files deleted"
fi

# prompt the user for if they are testing ENCUT or KPOINT convergence
while true; do
	# loop user input until valid
	echo "Would you like to test for ENCUT convergence or KPOINT convergence?"
	read -p "Type 'E' or 'K': " encut_or_kpoint_testing
	case $encut_or_kpoint_testing in
	 [Ee]* ) encut_or_kpoint_testing="encut" # make the user input uniform
	  break;;
	 [Kk]* ) encut_or_kpoint_testing="kpoint"  # make the user input uniform
	  break;;
	esac
done

# create spreadsheet to store data
touch results.csv
touch results.txt
# add data labels
echo "E0 ENCUT NxNxN-KPOINT-DENSITY" >results.txt

# run selected convergence function
case $encut_or_kpoint_testing in
 "encut")
  encutConvergence;; # run encut convergence function
 "kpoint")
  kpointConvergence;; # run kpoint convergence function
esac



