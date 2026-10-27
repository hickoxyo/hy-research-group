#=================================================================
# augsburg university
# hickox-young energy materials lab
# dos graphing tool
# jerid mcdonald '28, daniel hickox-young phd
# mcdona14@augsburg.edu
# this software graphs the density of states for atomic crystal structures. it focuses on ease of use and quality of life features. it is built for the hickox-young energy materials lab workflow.
# for full, granular control, edit the settings below
#=================================================================
"""
||=======================||
||EDIT USER SETTINGS HERE||
||=======================||
"""
'''
TO ADD: 
- per element graphing
- color per element
- opacity of each
- combine spin polarized colors
- txt file printout
- seperate out combining with graphing
'''

# [X]
# SAVED FILES
EXPORT_AS_CSV = True
save_figure = False
saved_name = 'dos_plot'
#'png', 'pdf', or 'svg'
file_type = 'png' 
display_preview_dpi = 200
figure_dpi = 500
transparency = True

# [/]
# COLORS
fill_color = "#7F7F7F"
dark_mode = False
#TODO: create array of color preferences
colors = ['#000000',"#df2020","#df9320","#93df20","#20df20","#20df93","#20dfdf","#2093df","#2020df","#9320df","#df2093"]

# [X]
# LINES
# MARKER STYLES:'' (none), '.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd', '|', or '_'
marker_style = ''
# LINE STYLES: '-' for solid, ':' for short dashed, '--' for long dashed, '-.' for long short long dash pattern
line_style = '-'
# 'butt', 'round', or 'projecting'
cap_style = 'butt'


# [X]
# AXIS LABELS
x_label = "Energy (eV)"
y_label = "Density of States  (states / eV)"

# [X]
# SCALE
#True or False
auto_scale = False
x_min = -13
x_max = 3.75
y_min = -30
y_max = 30

# [X]
# FIGURE SIZE
auto_size = False
figure_width_inches = 4
figure_height_inches = 7.5/2
# removed until further notice
#figure_unit = 'inch' # "inch", "cm", "px".

# [X]
# GENERAL TICKS
# #'in', or 'out'
tick_direction = 'in'
top_ticks = True
bottom_ticks = True
left_ticks = True
right_ticks = False

# [X]
# X TICKS
#   MAJOR
x_major_tick_multiple = 0 # 0 for auto
# tick direction: 'in', 'out', or 'inout'
x_major_tick_direction = 'in'  
x_major_tick_width = 2
x_major_tick_length = 5
# name or hexcode
x_major_tick_color = 'black'
#   MINOR
x_minor_tick_multiple = 0 # 0 for auto
# tick direction: 'in', 'out', or 'inout'
x_minor_tick_direction = 'in'  
x_minor_tick_width = 2
x_minor_tick_length = 3
# name or hexcode
x_minor_tick_color = 'black'

# [X]
# Y TICKS
#   MAJOR
y_major_tick_multiple = 0 #0 for auto
# tick direction: 'in', 'out', or 'inout'
y_major_tick_direction = 'in' 
y_major_tick_width = 2
y_major_tick_length = 5
# name or hexcode
y_major_tick_color = 'black'
#   MINOR
y_minor_tick_multiple = 0 #0 for auto
# tick direction: 'in', 'out', or 'inout'
y_minor_tick_direction = 'in' 
y_minor_tick_width = 2
y_minor_tick_length = 3
# name or hexcode
y_minor_tick_color = 'black'

# [X]
# SPINES (outer edges of the graph)
top_spine_line_width = 1.1
left_spine_line_width = 1.1
right_spine_line_width = 1.1
bottom_spine_line_width = 1.1

# [X]
# GRAPH FORMAT
# leave blank for no title. latex format compatitble (ie. title = r'$\sigma_i=15$')
title = ''
remove_tick_labels = False
hide_legend = False
hide_legend_border = False

# [X]
# FERMI LEVEL
show_fermi_level = True
# color is in hex code
fermi_level_color = "#000000"
fermi_level_max_height = 75
# line styles: 'solid', 'dashed', 'dashdot', or 'dotted'
fermi_level_line_style = 'dashed' 

# combine duplicate elements?
COMBINE_DUPLICATE_ELEMENTS = False

# [ ]
#array of specific elements to graph
# color_array=[red, blue]
USE_CUSTOM_ELEMENTS = False

USE_CUSTOM_ORBITALS = False

USE_CUSTOM_SUBORBITALS = False

SPIN_POLARIZED = True

"""
======================================================================================
|| ------------------------- MAIN SOFTWARE BELOW -----------------------------------||
======================================================================================
"""

"""
TODO:
+ get defualt colors from Daniel
+ spin polarized
+ custom elements   
 -Parse DOS
    +ASSUMES WE WILL NEVER HAVE A DOUBLE DIGIT NUMBER AFTER AN ELEMENT
"""
import matplotlib.pyplot as plt
from pathlib import Path
import copy
import csv
import os

def initialize_graph_settings():
    # initialize figure and ax objects
    element_figure, ax = plt.subplots(figsize = (float(figure_height_inches), float(figure_width_inches)), dpi = display_preview_dpi)

    # DOS fill
    if SPIN_POLARIZED == False:
        ax.fill_between(global_element_dictionary['Total DOS']['energy'], global_element_dictionary['Total DOS']['dos'], color = fill_color, alpha = 0.2, label = 'Total DOS')#, figure = element_name)
    if SPIN_POLARIZED == True:
        ax.fill_between(global_element_dictionary['Total DOS']['energy'], global_element_dictionary['Total DOS']['dos_up'], color = fill_color, alpha = 0.2, label = 'Total DOS')#, figure = element_name)
        ax.fill_between(global_element_dictionary['Total DOS']['energy'], global_element_dictionary['Total DOS']['dos_down'], color = fill_color, alpha = 0.2, label = 'Total DOS')#, figure = element_name)


    if show_fermi_level == True:
        # check for negative graph values
        if SPIN_POLARIZED == True:
            ymin = fermi_level_max_height * -1

        else:
            ymin = 0

        plt.vlines(x= 0, ymin= ymin, ymax= fermi_level_max_height, colors= fermi_level_color, linestyles= fermi_level_line_style, label= "Fermi Level")

    # labels
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)


    # general tick parameters
    ax.tick_params(which = 'both', direction = tick_direction, top = top_ticks, bottom = bottom_ticks, left = left_ticks, right = right_ticks)

    # x ticks
    # TODO
    if x_major_tick_multiple != 0:
        ax.xaxis.set_major_locator(plt.MultipleLocator(x_major_tick_multiple))
    if x_minor_tick_multiple != 0:    
        ax.xaxis.set_minor_locator(plt.MultipleLocator(x_minor_tick_multiple))
    ax.tick_params(axis = 'x', which = 'major', direction = x_major_tick_direction, width = x_major_tick_width, length = x_major_tick_length, color = x_major_tick_color)
    ax.tick_params(axis = 'x', which = 'minor', direction = x_minor_tick_direction, width = x_minor_tick_width, length = x_minor_tick_length, color = x_minor_tick_color)

    # y ticks
    # TODO

    if y_major_tick_multiple != 0:
        ax.yaxis.set_major_locator(plt.MultipleLocator(y_major_tick_multiple))
    if y_minor_tick_multiple != 0:    
        ax.yaxis.set_minor_locator(plt.MultipleLocator(y_minor_tick_multiple))
    ax.tick_params(axis = 'y', which = 'major', direction = y_major_tick_direction, width = y_major_tick_width, length = y_major_tick_length, color = y_major_tick_color)
    ax.tick_params(axis = 'y', which = 'minor', direction = y_minor_tick_direction, width = y_minor_tick_width, length = y_minor_tick_length, color = y_minor_tick_color)

    if remove_tick_labels == True:
        ax.set_xticklabels([])
        ax.set_yticklabels([])

    # manual scale
    if auto_scale == False:
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)

    # outer graph box (each edge called a 'spine')
    ax.spines['top'].set_linewidth(top_spine_line_width)
    ax.spines['left'].set_linewidth(left_spine_line_width)
    ax.spines['right'].set_linewidth(right_spine_line_width)
    ax.spines['bottom'].set_linewidth(bottom_spine_line_width)

    # figure size
    if auto_size == False:
        element_figure.set_size_inches(figure_width_inches, figure_height_inches)

    # dark mode
    if dark_mode == True:
        plt.style.use('dark_background')
    
    #title
    plt.title(title)

    return element_figure, ax

def save_figure_check(element_figure):
    if save_figure == True:
            # makes sure not to overwrite existing files
            i = 0  
            file_name = Path(saved_name + '.' + file_type)
            while file_name.exists():
                i += 1
                file_name = Path(saved_name + str(i) + '.' + file_type)

            plt.figure(element_figure)
            plt.savefig(file_name, transparent = transparency, format = file_type, dpi = figure_dpi)

def parse_DOS(DOS_file):
    '''
    OVERVIEW
    reads header and sets up a number of variables with names equal to their element and number.
    if there is a number after the element it means that many atoms are present. 
    we label each seperately:
    ie. H2O would be H, O1, O2

    reads file lines until the value in the first column (energy) is the same as the previous line. 
    this denotes that the data set has ended and a new one is beginning
    '''
    # open and read DOSCAR
    file = open(DOS_file)
    content = file.readlines()

    # get the fermi level
    global fermi_level
    fermi_level = (content[5]).strip().split()
    fermi_level = float(fermi_level[3])

    # declare variables
    # the first set of data listed in the DOSCAR is the total energy data, so we initialize the element list to start with that 
    element_list = ["Total DOS"]
    temp_element = ""
    global global_element_dictionary
    global_element_dictionary = {}
    orbital_dictionary = {}
    results_dicitonary = {}
    # initialize dictionary with empty values
    global regular_orbital_keys
    regular_orbital_keys = ['energy', 's1', 'p1', 'p2', 'p3', 'd1', 'd2', 'd3', 'd4', 'd5', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7']
    global spin_polarized_orbital_keys
    spin_polarized_orbital_keys = ['energy', 's1_up', 's1_down',
                                   'p1_up', 'p1_down', 'p2_up', 'p2_down', 'p3_up', 'p3_down',
                                   'd1_up', 'd1_down', 'd2_up', 'd2_down', 'd3_up', 'd3_down', 'd4_up', 'd4_down', 'd5_up', 'd5_down',
                                   'f1_up', 'f1_down', 'f2_up', 'f2_down', 'f3_up', 'f3_down', 'f4_up', 'f4_down', 'f5_up', 'f5_down', 'f6_up', 'f6_down', 'f7_up', 'f7_down'
                                  ]

    if SPIN_POLARIZED == True:
        # spin polarized
        for key in spin_polarized_orbital_keys:
            orbital_dictionary[key] = []
            orbital_keys = spin_polarized_orbital_keys
    else:
        # not spin polarized
        for key in regular_orbital_keys:
            orbital_dictionary[key] = []
            orbital_keys = regular_orbital_keys

    # identify elements and load them into dictionaries
    # content[4] are the element names listed in the DOSCAR
    file_line = 4
    for char in content[file_line]:
        # check for new element
        if char.isupper():
            # if buffer is blank, don't add it
            if temp_element != "":
                # append buffer to element list
                element_list.append(temp_element)

            # reset buffer starting with the new element's first letter
            temp_element = char

        # if lower, add to current element
        elif char.islower():
            temp_element += char

        # ASSUMES WE WILL NEVER HAVE A DOUBLE DIGIT NUMBER AFTER AN ELEMENT
        #TODO: fix this ^
            '''
            makes a unique element entry based on the number after the element
            i.e. CsPbBr3 would return Cs, Pb, Br1, Br2, Br3
            '''
        elif char.isnumeric():
            i = 1
            temp_recursive_element = ""
            while i <= int(char):
                temp_recursive_element = temp_element + '_' + str(i)
                element_list.append(temp_recursive_element)
                i+=1

            temp_element = ""

        else:
            if temp_element != "":
                element_list.append(temp_element)
                temp_element = ""

            else:
                pass

    # get past energy header
    file_line += 2
    # start assigning DOS values to elements
    for element in element_list:
        # initialize empty element dictionary
        global_element_dictionary[element] = None
        # loop through data set
        if SPIN_POLARIZED == False:
            if element == "Total DOS":
                '''
                Three data columns: energy | DOS | integrated_DOS
                '''
                # declare variables
                energy_array = []
                dos_array = []
                integrated_dos_array = []
                i = 0
                # loop through the columns and append them to their own arrays
                while True:
                    # parse doscar lines
                    try:
                        current_line_values = content[file_line].strip().split()

                    except:
                        break
                    '''
                    Check if the next energy level was the same as the last
                    This happens when a section has finished its tests from -15 to 15 (before adjusting for the fermi level)
                    '''
                    try:
                        if (float(current_line_values[0]) - fermi_level) == (float(energy_array[len(energy_array)-1])):
                            # incriment past the energy header for the next section
                            file_line += 1
                            break

                    except IndexError: # we expect an index error when no values have been added to the array yet
                        pass

                    # append DOS variables
                    energy_array.append(float(current_line_values[0]) - fermi_level)  # adjusted for fermi level
                    dos_array.append(float(current_line_values[1]))
                    integrated_dos_array.append(float(current_line_values[2]))
                    file_line += 1
            
                # compile results into a dictionary
                results_dicitonary['energy'] = energy_array
                results_dicitonary['dos'] = dos_array
                results_dicitonary['integrated_dos'] = integrated_dos_array
                global_element_dictionary[element] = results_dicitonary

            else:
                '''
                Parses all 16 potential orbitals
                '''
                while True:
                    try:
                        # parse data from DOSCAR
                        current_line_values = content[file_line].strip().split()

                    except IndexError: # end of file
                        break
                    
                    '''
                    Check if the next energy level was the same as the last
                    This happens when a section has finished its tests from -15 to 15 (before adjusting for the fermi level)
                    '''
                    try:
                        if (float(current_line_values[0]) - fermi_level) == float(orbital_dictionary['energy'][-1]):  
                            # incriment past the energy header for the next section
                            file_line += 1
                            break

                    except IndexError: # empty array
                            pass
                    
                    # iterate through a nested loop of orbital values from the DOSCAR, and add them to their appropriate orbital dictionary
                    i = 0 # for indexing within the current_line_values array
                    for orbital_label in orbital_keys:
                        if i < len(current_line_values): #for orbital_value in current_line_values:
                            # check if the array needs to be created vs appended to
                            if orbital_label == 'energy':
                                try:
                                    orbital_dictionary[orbital_label].append(float(current_line_values[i]) - fermi_level)

                                except AttributeError:
                                    orbital_dictionary[orbital_label] = float(current_line_values[i] - fermi_level)
                                                        
                            else:    
                                try:
                                    orbital_dictionary[orbital_label].append(float(current_line_values[i]))

                                except AttributeError:
                                    orbital_dictionary[orbital_label] = float(current_line_values[i])
                            i += 1     

                        else:
                            break

                    # incriment file line
                    file_line += 1

                # write orbitals data to dictionary
                global_element_dictionary[element] = copy.deepcopy(orbital_dictionary)
                # reset dictionary
                for key in orbital_keys:
                    orbital_dictionary[key] = []


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        if SPIN_POLARIZED == True:
            if element == "Total DOS":
                '''
                Five data columns:  energy  |  DOS(up)  |  DOS(dwn)  |  integrated DOS(up)  |  integrated DOS(dwn)
                '''
                # declare variables
                energy_array = []
                dos_up_array = []
                dos_down_array = []
                integrated_dos_up_array = []
                integrated_dos_down_array = []
                i = 0
                # loop through the columns and append them to their own arrays
                while True:
                    # parse doscar lines
                    try:
                        current_line_values = content[file_line].strip().split()

                    except:
                        break
                    '''
                    Check if the next energy level was the same as the last
                    This happens when a section has finished its tests from -15 to 15 (before adjusting for the fermi level)
                    '''
                    try:
                        if (float(current_line_values[0]) - fermi_level) == (float(energy_array[len(energy_array)-1])):
                            # incriment past the energy header for the next section
                            file_line += 1
                            break

                    except IndexError: # we expect an index error when no values have been added to the array yet
                        pass

                    # append DOS variables
                    energy_array.append(float(current_line_values[0]) - fermi_level)  # adjusted for fermi level
                    dos_up_array.append(float(current_line_values[1]))
                    dos_down_array.append(float(current_line_values[2]) * -1) 
                    integrated_dos_up_array.append(float(current_line_values[3])) 
                    integrated_dos_down_array.append(float(current_line_values[4]) * -1) 

                    file_line += 1
            
                # compile results into a dictionary
                results_dicitonary['energy'] = energy_array
                results_dicitonary['dos_up'] = dos_up_array
                results_dicitonary['dos_down'] = dos_down_array
                results_dicitonary['integrated dos_up'] = integrated_dos_up_array
                results_dicitonary['integrated dos_down'] = integrated_dos_down_array
                global_element_dictionary[element] = results_dicitonary

            else:
                '''
                Parses all 16 potential orbitals
                '''
                while True:
                    try:
                        # parse data from DOSCAR
                        current_line_values = content[file_line].strip().split()

                    except IndexError: # end of file
                        break
                    
                    '''
                    Check if the next energy level was the same as the last
                    This happens when a section has finished its tests from -15 to 15 (before adjusting for the fermi level)
                    '''
                    try:  
                        if (float(current_line_values[0]) - fermi_level) == float(orbital_dictionary['energy'][-1]):  
                            # incriment past the energy header for the next section
                            file_line += 1
                            break

                    except IndexError: # empty array
                            pass
                    
                    # iterate through a nested loop of orbital values from the DOSCAR, and add them to their appropriate orbital dictionary
                    i = 0 # for indexing within the current_line_values array
                    for orbital_label in spin_polarized_orbital_keys:
                        if i < len(current_line_values): #for orbital_value in current_line_values:
                            # check if the array needs to be created vs appended to
                            if orbital_label == 'energy':
                                try:
                                    orbital_dictionary[orbital_label].append(float(current_line_values[i]) - fermi_level)

                                except AttributeError:
                                    orbital_dictionary[orbital_label] = float(current_line_values[i] - fermi_level)
                                                        
                            else:

                                # spin up
                                if 'up' in orbital_label:
                                    
                                    try:
                                        orbital_dictionary[orbital_label].append(float(current_line_values[i]))

                                    except AttributeError:
                                        orbital_dictionary[orbital_label] = float(current_line_values[i])


                                # make values negative
                                elif 'down' in orbital_label:
                                    try:
                                        orbital_dictionary[orbital_label].append(float(current_line_values[i]) * -1)

                                    except AttributeError:
                                        orbital_dictionary[orbital_label] = float(current_line_values[i] * -1)





                            i += 1     

                        else:
                            break

                    # incriment file line
                    file_line += 1

                # write orbitals data to dictionary
                global_element_dictionary[element] = copy.deepcopy(orbital_dictionary)
                # reset dictionary
                for key in orbital_keys:
                    orbital_dictionary[key] = []

        

    return global_element_dictionary   

def duplicate_element_check(element_dictionary):
    # declare and initialize our variables
    names_combined_elements_parent_array = []
    names_combined_elements_child_array = []
    element_current = ''
    element_buffer = ''
    element_tracker = ''
    last_element = ''
    first_iteration_per_element = True
    duplicate_element = False

    for element in element_dictionary:
        # Total DOS is handled seperately
        if element == 'Total DOS':
            continue

        for char in element:
            # check if the character is a letter
            if char.isalpha():
                #check if  character is uppercase (ie start of an element)
                if char.isupper():
                    if element_tracker != element_current:
                        # reset for new element
                        first_iteration_per_element = True
                        duplicate_element = False
                        # avoid appending empty arrays
                        if element_current != '' and names_combined_elements_child_array != []:
                            names_combined_elements_parent_array.append(names_combined_elements_child_array)

                        # reset child array
                        names_combined_elements_child_array = []

                    # assign the last element to the buffer to check duplicates against. If there is no element yet then this line does nothing
                    element_buffer = element_current
                    # tracker is used to tell if there are multiple duplicate elements that need to be summed seperately
                    element_tracker = element_current
                    # reset the element
                    element_current = ''

                element_current += char

            # if the next character is lowercase, compare it to the buffer
            else:
                 # check for duplicate element
                 if element_buffer == element_current:
                    duplicate_element = True
                    # makes sure all duplicates are properly added
                    if first_iteration_per_element == True:
                        # adds element to list
                        names_combined_elements_child_array.append(last_element)
                        names_combined_elements_child_array.append(element)
                        first_iteration_per_element = False

                    else:
                        if names_combined_elements_child_array[-1] != element:
                            names_combined_elements_child_array.append(element)

                    last_element = element

        # remember the last element to assign later if needed
        last_element = element

    # catches if the last element is a duplicate
    if duplicate_element == True:
        names_combined_elements_parent_array.append(names_combined_elements_child_array)

    return names_combined_elements_parent_array

def duplicate_element_combination(element_dictionary):
    # declare variables
    element_dictionary_present = True
    if element_dictionary == None:
        element_dictionary = global_element_dictionary
        element_dictionary_present = False

    if SPIN_POLARIZED == True:
        orbital_keys = spin_polarized_orbital_keys
    else:
        orbital_keys = regular_orbital_keys

    element_name_array = duplicate_element_check(element_dictionary)
    combined_element_dictionary = {}
    # repeat process for each unique element present
    for element_category in element_name_array:
        i = 0
        longform_element_name = element_category[0]
        element_name = str(element_category[0]).split('_')[0]
        combined_element_dictionary[element_name] = {}
        for orbital in orbital_keys:
            combined_element_dictionary[element_name][orbital] = []

        # transfer fermi-adjusted energy levels
        combined_element_dictionary[element_name]['energy'] = element_dictionary[longform_element_name]['energy']

        while i < len(list(element_dictionary[longform_element_name]['energy'])):
            for element in element_category:
                for orbital in orbital_keys: # global variable
                    # combine duplicate elements
                    if element_name in element:
                        if orbital == 'energy':
                            combined_element_dictionary[element_name][orbital][i]
                            continue

                        try:
                            combined_element_dictionary[element_name][orbital][i] += float(element_dictionary[element][orbital][i])
                        
                        except IndexError: # non-existant array
                            try:
                                combined_element_dictionary[element_name][orbital].append(float(element_dictionary[element][orbital][i]))
                            except IndexError: # no f orbitals for the element
                                pass
            i += 1        

    if element_dictionary_present == True:
        reinserted_element_dictionary = reinsert_element(combined_element_dictionary, element_dictionary)

    else:
        reinserted_element_dictionary = reinsert_element(combined_element_dictionary)

    return reinserted_element_dictionary

def reinsert_element(combined_element_dictionary, element_dictionary):
    if element_dictionary == None:
        element_dictionary = global_element_dictionary
    
    # find what to remove
    for combined_element in combined_element_dictionary:
        i = 0
        elements_to_remove = []
        # split element name seperately for ease of readability
        element_keys = list(element_dictionary.keys())
        while i < len(element_dictionary):
            # compare name of combined_element to adjusted element name in element_dictionary
            element = str(element_keys[i]).split('_')[0]
            if combined_element == element:
                elements_to_remove.append(i)

            i+=1

        # do the removing
        element_dictionary = list(element_dictionary.items())
        # seperate into variables for ease of reading
        start = elements_to_remove[0]
        stop = elements_to_remove[-1]
        element_to_add = combined_element_dictionary[combined_element]#.items()
        # cut out the duplicate elements and add the combined element
        element_dictionary[start:stop + 1] = [(combined_element, element_to_add)]
        # convert back to dictionary
        element_dictionary = dict(element_dictionary)

    return element_dictionary

def graph_by_suborbital(element_dictionary):
        if element_dictionary == None:
            element_dictionary = global_element_dictionary

        if COMBINE_DUPLICATE_ELEMENTS == True:
            element_dictionary = duplicate_element_combination(element_dictionary)

    
        for element in element_dictionary:
            # total DOS is filled between seperately 
            if element == "Total DOS":
                # export total DOS data to a csv.
                with open('totalDOS.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(list(element_dictionary['Total DOS'].keys()))
                    writer.writerows(zip(*element_dictionary['Total DOS'].values()))

                continue

            #initialize graph settings
            if dark_mode == True:
                    plt.style.use('dark_background')

            element_figure, ax = initialize_graph_settings()
            ax.legend(ncols = 3)
            for orbital in element_dictionary[element]:
                if orbital != 'energy': 
                    try:
                        # rewritten as variables for debugging and ease of reading
                        temp_x = element_dictionary[element]['energy']
                        temp_y = element_dictionary[element][orbital]
                        label = element + " " + orbital
                        plt.figure(element_figure)
                        '''
                        # labels are in latex notation using the following syntax:
                        # '$\ [Latex notation] $
                        '''
                        match orbital:
                            case 's1':
                                label = r'$\ ' + element + r'\ s$'
                            case 'p1':
                                label = r'$\ ' + element + r'\ p_y$'
                            case 'p2':
                                label = r'$\ ' + element + r'\ p_z$'
                            case 'p3':
                                label = r'$\ ' + element + r'\ p_x$'
                            case 'd1':
                                label = r'$\ ' + element + r'\ d_{x^2 - y^2}$'
                            case 'd2':
                                label = r'$\ ' + element + r'\ d_{yz}$'
                            case 'd3':
                                label = r'$\ ' + element + r'\ d_{z^2}$'
                            case 'd4':
                                label = r'$\ ' + element + r'\ d_{xz}$'
                            case 'd5':
                                label = r'$\ ' + element + r'\ d_{xy}$'
                            case 'f1':
                                label = r'$\ ' + element + r'\ f_{y(3x^2 - y^2)}$'
                            case 'f2':
                                label = r'$\ ' + element + r'\ f_{z(x^2 - y^2)}$'                                                                                                
                            case 'f3':
                                label = r'$\ ' + element + r'\ f_{yz^2}$'
                            case 'f4':
                                label = r'$\ ' + element + r'\ f_{z^3}$'
                            case 'f5':
                                label = r'$\ ' + element + r'\ f_{xz^2}$'
                            case 'f6':
                                label = r'$\ ' + element + r'\ f_{xyz}$'
                            case 'f7':
                                label = r'$\ ' + element + r'\ f_{x(x^2 - 3y^2)}$'

                        plt.plot(temp_x, temp_y, label = label, marker = marker_style, linestyle = line_style, dash_capstyle = cap_style)

                        if hide_legend_border == True:
                            plt.legend(frameon = False)

                        plt.legend() 
                        ax.legend(ncols = 3)

                        if hide_legend == True:
                            ax.legend().set_visible(False)

                    except IndexError and ValueError:
                        pass

                filename = element + "_suborbitals.csv"
                with open (filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
            # export as csv
                    if SPIN_POLARIZED:
                        
                        writer.writerow(['s1_up', 's1_down', 'p1_up', 'p1_down', 'p2_up', 'p2_down', 'p3_up', 'p3_down', 'd1_up', 'd1_down', 'd2_up', 'd2_down', 'd3_up', 'd3_down',
                                        'd4_up', 'd4_down', 'd5_up', 'd5_down', 'f1_up', 'f1_down', 'f2_up', 'f2_down', 'f3_up', 'f3_down', 'f4_up', 'f4_down', 'f5_up', 'f5_down',
                                        'f6_up', 'f6_down', 'f7_up', 'f7_down'])
                        sums_to_be_zipepd=[]
                        for value in element_dictionary[element].values():
                            if value !=[]:
                                sums_to_be_zipepd.append(value)
                        writer.writerows(zip(*sums_to_be_zipepd))
                    else:
                        
                        writer.writerow(['s1', 'p1', 'p2', 'p3', 'd1', 'd2', 'd3', 'd4', 'd5', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7'])
                        sums_to_be_zipepd=[]
                        for value in element_dictionary[element].values():
                            if value !=[]:
                                sums_to_be_zipepd.append(value)
                        writer.writerows(zip(*sums_to_be_zipepd))

            save_figure_check(element_figure)

def graph_by_orbital(element_dictionary):
    if element_dictionary == None:
        element_dictionary = global_element_dictionary

    if COMBINE_DUPLICATE_ELEMENTS == True:
        element_dictionary = duplicate_element_combination(element_dictionary)

    for element in element_dictionary:
        try:
            # 'Total DOS' is handled seperately
            if element == 'Total DOS':
                # export total DOS data to a csv.
                with open('totalDOS.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    #TODO: check the zip unpack function
                    writer.writerow(list(element_dictionary['Total DOS'].keys()))
                    writer.writerows(zip(*element_dictionary['Total DOS'].values()))

                                
                continue

            # initialize graph settings
            if dark_mode == True:
                    plt.style.use('dark_background')

            element_figure, ax = initialize_graph_settings()
            # SHELLS
            # only submit one element at a time
            temp_orbital_sum_dictionary = orbital_shell_sums(element_dictionary[element])
            # plot summed orbitals against energy            
            for shell in temp_orbital_sum_dictionary:
                if shell == 'energy':
                    continue

                try:
                    plt.plot(temp_orbital_sum_dictionary['energy'],temp_orbital_sum_dictionary[shell], label = r"$\ " + element + r"\ " + shell + "$", figure = element_figure,
                             marker = marker_style, linestyle = line_style, dash_capstyle = cap_style)
                    ax.legend()

                except ValueError as error:
                    print("No orbital at", element, shell)

                if hide_legend_border == True:
                    plt.legend(frameon = False)

                if hide_legend == True:
                    plt.legend().remove()

            if EXPORT_AS_CSV:
                filename = element + '_orbitals.csv'
                with open (filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # energy = element_dictionary[element]['energy']

                    if SPIN_POLARIZED:

                        writer.writerow(['energy', 's_up', 's_down', 'p_up', 'p_down', 'd_up', 'd_down', 'f_up', 'f_down'])
                        to_be_zipped_sums = []
                        for item in temp_orbital_sum_dictionary.values():
                            if item != []:
                                to_be_zipped_sums.append(item)
                        writer.writerows(zip(*to_be_zipped_sums))
                

                    else:
                        writer.writerow(['energy', 's', 'p', 'd', 'f'])
                        to_be_zipped_sums = []
                        for item in temp_orbital_sum_dictionary.values():
                            if item != []:
                                to_be_zipped_sums.append(item)
                        writer.writerows(zip(*to_be_zipped_sums))
            # plt.show()
            save_figure_check(element_figure)

        except TypeError as error:
                print(error)

def graph_by_element(element_dictionary):
    if element_dictionary == None:
        element_dictionary = global_element_dictionary

    if COMBINE_DUPLICATE_ELEMENTS == True:
        element_dictionary = duplicate_element_combination(element_dictionary)

    # iniitalize graph settings
    #TODO: see if this needs to stay here
    if dark_mode == True:
        plt.style.use('dark_background')

    element_figure, ax = initialize_graph_settings()

    # create an empty dictionary to store and label the element sums
    element_sum_dictionary = {}

    # submit one element at a time
    for element in element_dictionary:    
        try:
            # call the graphing function
            if element == 'Total DOS':
                
                # export total DOS data to a csv.
                with open('totalDOS.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)

                    #TODO: check the zip unpack function
                    writer.writerow(list(element_dictionary['Total DOS'].keys()))
                    writer.writerows(zip(*element_dictionary['Total DOS'].values()))

                continue

            element_sum_dictionary[element] = element_sums(element_dictionary[element])


            if SPIN_POLARIZED == True:
                 # call the figure we created settings for
                plt.plot(element_dictionary[element]['energy'], element_sum_dictionary[element]['spin_up'], label = r'$\ ' + element + '$', figure = element_figure, 
                        marker = marker_style, linestyle = line_style, dash_capstyle = cap_style)
                plt.plot(element_dictionary[element]['energy'], element_sum_dictionary[element]['spin_down'], label = r'$\ ' + element + '$', figure = element_figure, 
                        marker = marker_style, linestyle = line_style, dash_capstyle = cap_style)

                ax.legend()

                if hide_legend_border == True:
                    ax.legend(frameon = False)
                if hide_legend == True:
                    plt.legend().remove()
                
            else:
                # call the figure we created settings for
                plt.plot(element_dictionary[element]['energy'], element_sum_dictionary[element], label = r'$\ ' + element + '$', figure = element_figure, 
                        marker = marker_style, linestyle = line_style, dash_capstyle = cap_style)

                ax.legend()

                if hide_legend_border == True:
                    ax.legend(frameon = False)
                if hide_legend == True:
                    plt.legend().remove()

                
            
            # ax.legend()
            if EXPORT_AS_CSV:
                filename = element + '.csv'
                with open (filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    energy = element_dictionary[element]['energy']

                    if SPIN_POLARIZED:
                        writer.writerow(['energy', 'spin_up', 'spin_down'])
                        writer.writerows(zip(energy, element_sum_dictionary[element]['spin_up'], element_sum_dictionary[element]['spin_down']))
            
        except TypeError as error:
            print(error)



    save_figure_check(element_figure)
    # plt.show()






#SUBMIT ONE ELEMENT AT A TIME
def orbital_shell_sums(orbital_dictionary):
    if SPIN_POLARIZED == True:
        shell_totals = {'energy':[], 's_up':[], 's_down':[], 'p_up':[], 'p_down':[], 'd_up':[], 'd_down':[], 'f_up':[], 'f_down':[]}
        # START WITH SUMMING BY SHELL
        i = 0
        for i in range(len(orbital_dictionary['energy'])):
            try:
                shell_totals['energy'].append(orbital_dictionary['energy'][i])
                shell_totals['s_up'].append(orbital_dictionary['s1_up'][i])
                shell_totals['s_down'].append(orbital_dictionary['s1_down'][i])
                shell_totals['p_up'].append(orbital_dictionary['p1_up'][i] + orbital_dictionary['p2_up'][i] + orbital_dictionary['p3_up'][i])

                shell_totals['p_down'].append(orbital_dictionary['p1_down'][i] + orbital_dictionary['p2_down'][i] + orbital_dictionary['p3_down'][i])

                shell_totals['d_up'].append(orbital_dictionary['d1_up'][i] + orbital_dictionary['d2_up'][i] + orbital_dictionary['d3_up'][i]
                                    + orbital_dictionary['d4_up'][i] + orbital_dictionary['d5_up'][i])

                shell_totals['d_down'].append(orbital_dictionary['d1_down'][i] + orbital_dictionary['d2_down'][i] + orbital_dictionary['d3_down'][i]
                                    + orbital_dictionary['d4_down'][i] + orbital_dictionary['d5_down'][i])

                shell_totals['f_up'].append(orbital_dictionary['f1_up'][i] + orbital_dictionary['f2_up'][i] + orbital_dictionary['f3_up'][i]
                                    + orbital_dictionary['f4_up'][i] + orbital_dictionary['f5_up'][i] + orbital_dictionary['f6_up'][i] 
                                    + orbital_dictionary['f7_up'][i])

                shell_totals['f_down'].append(orbital_dictionary['f1_down'][i] + orbital_dictionary['f2_down'][i] + orbital_dictionary['f3_down'][i]
                                    + orbital_dictionary['f4_down'][i] + orbital_dictionary['f5_down'][i] + orbital_dictionary['f6_down'][i] 
                                    + orbital_dictionary['f7_down'][i])


                i+=1

            except (IndexError, KeyError) as error: # nonesistant array
                # i+=1
                print(error)
                continue
    
    if SPIN_POLARIZED == False:
        shell_totals = {'energy':[], 's':[], 'p':[], 'd':[], 'f':[]}
        # START WITH SUMMING BY SHELL
        i = 0
        for i in range(len(orbital_dictionary['energy'])):
            try:
                shell_totals['energy'].append(orbital_dictionary['energy'][i])
                shell_totals['s'].append(orbital_dictionary['s1'][i])
                shell_totals['p'].append(orbital_dictionary['p1'][i] + orbital_dictionary['p2'][i] + orbital_dictionary['p3'][i])
                shell_totals['d'].append(orbital_dictionary['d1'][i] + orbital_dictionary['d2'][i] + orbital_dictionary['d3'][i]
                                    + orbital_dictionary['d4'][i] + orbital_dictionary['d5'][i])
                shell_totals['f'].append(orbital_dictionary['f1'][i] + orbital_dictionary['f2'][i] + orbital_dictionary['f3'][i]
                                    + orbital_dictionary['f4'][i] + orbital_dictionary['f5'][i] + orbital_dictionary['f6'][i] 
                                    + orbital_dictionary['f7'][i])
                i+=1

            except (IndexError, KeyError) as error: # nonesistant array
                # i+=1
                print(error)
                continue

    return shell_totals

#SUBMIT ONE ELEMENT AT A TIME
def element_sums(orbital_dictionary):
    element_sum_dictionary = {}
    temp_element_sums = []
    temp_element_sums_up = []
    temp_element_sums_down = []
    temp_shell_sums = orbital_shell_sums(orbital_dictionary)

    if SPIN_POLARIZED == True:
        for i in range(len(orbital_dictionary['energy'])):
            try:
                # try them one at a time
                # energy = list(temp_shell_sums['energy'])
                temp_element_sums_up.append(0)
                temp_element_sums_down.append(0)
                temp_element_sums_up[i] += temp_shell_sums['s_up'][i] 
                temp_element_sums_down[i] += temp_shell_sums['s_down'][i]
                temp_element_sums_up[i] += temp_shell_sums['p_up'][i]
                temp_element_sums_down[i] += temp_shell_sums['p_down'][i]
                temp_element_sums_up[i] += temp_shell_sums['d_up'][i]
                temp_element_sums_down[i] += temp_shell_sums['d_down'][i] 
                temp_element_sums_up[i] += temp_shell_sums['f_up'][i] 
                temp_element_sums_down[i] += temp_shell_sums['f_down'][i]

            except (ValueError, IndexError) as error:
                print("No shell found at", error)
                pass
         #TODO: if I wanted to put them in dictionaries instead and label them, I would do that here
        element_sum_dictionary['spin_up'] = temp_element_sums_up
        element_sum_dictionary['spin_down'] = temp_element_sums_down

    else:
        for i in range(len(orbital_dictionary['energy'])):
            try:
                # try them one at a time
                # energy = list(temp_shell_sums['energy'])
                temp_element_sums.append(0)
                temp_element_sums[i] += temp_shell_sums['s'][i] 
                temp_element_sums[i] += temp_shell_sums['p'][i] 
                temp_element_sums[i] += temp_shell_sums['d'][i] 
                temp_element_sums[i] += temp_shell_sums['f'][i] 

            except (ValueError, IndexError) as error:
                print("No shell found at", error)
                pass
        element_sum_dictionary['total dos'] = temp_element_sums
    return element_sum_dictionary







def parse_CSV():
    # list folder contents 
    directory_contents = os.listdir()
    for file in directory_contents:
        if file.endswith('.csv'):
            # if csv read file
            with open(file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                labels = next(reader)
                csv_data = list(zip(*reader))
                print (labels)
                print(csv_data)




'''
for suborbityals:
if the first letter of the dictionary key is the same as the first letter of the previous dictionary key, combine the entries into the same csv
    append the duplicate letter entry to the csv


with open('names.csv', 'w', newline='') as csvfile:
fieldnames = ['first_name', 'last_name']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

writer.writeheader()
writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

'''















if __name__ == "__main__":
    try:
        element_dictionary = parse_DOS('DOSCAR')

        print("Processing...")





        
        graph_by_suborbital(element_dictionary) 
        # graph_by_orbital(element_dictionary)   
        #graph_by_element(element_dictionary)
        parse_CSV()

        print("Displaying...")

        plt.show()
        print("Finsihed")
        

    except FileNotFoundError:
        print("ERROR: DOSCAR file not found in current folder.")
    