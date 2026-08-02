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
opacity of each
'''
# [X]
# SAVED FILES
save_figure = True
saved_name = 'URGO_dos_plot'
#'png', 'pdf', or 'svg'
file_type = 'png' 
display_preview_dpi = 200
figure_dpi = 1000
transparency = True

# [/]
# COLORS
fill_color = "#7F7F7F"
dark_mode = False
#TODO: create array of color preferences

# [ ]
# LINES
# ARE LINE STYLES NEEDED?==================================================================================
# '-' for solid, ':' for short dashed, '--' for long dashed, '-.' for long short long dash pattern
line_style = '-'
# 'butt', 'round', or 'projecting'
cap_style = 'projecting'


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
y_min = -0.75
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

# [ ]
# X TICKS
x_major_tick_multiple = 1
x_minor_tick_multiple = 1 
x_major_tick_width = 2
x_major_tick_length = 10
x_major_tick_color = 'black'
x_minor_tick_width = 2
x_minor_tick_length = 5
x_minor_tick_color = 'black'

# [ ]
# Y TICKS
y_major_tick_multiple = 5
y_minor_tick_multiple = 1
y_major_tick_width = 2
y_major_tick_length = 10
y_major_tick_color = 'black'
y_major_tick_width = 2
y_major_tick_length = 10
y_major_tick_color = 'black'

# [X]
# SPINES (outer edges of the graph)
top_spine_line_width = 1.1
left_spine_line_width = 1.1
right_spine_line_width = 1.1
bottom_spine_line_width = 1.1

# [/]
# GRAPH FORMAT
# leave blank for no title
title = ''
#-------
remove_tick_labels = False
hide_legend_border = False

# [X]
# FERMI LEVEL
show_fermi_level = True
# color is in hex code
fermi_level_color = "#000000"
fermi_level_max_height = 75
#'solid', 'dashed', 'dashdot', or 'dotted'
fermi_level_line_style = 'dashed'

# [ ]
#array of specific elements to graph
USE_CUSTOM_ELEMENTS = False

USE_CUSTOM_ORBITALS = False

USE_CUSTOM_SUBORBITALS = False


"""
TODO:
+ settings
    +background and border
        facecolor = "white"
        edgecolor = "white"
    + DOS transparency - 7/28
+clean up code - 7/11
"""
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt
from pathlib import Path
#import numpy as np
import copy


def initialize_graph_settings():
    # initialize figure and ax objects
    element_figure, ax = plt.subplots(figsize = (float(figure_height_inches), float(figure_width_inches)), dpi = display_preview_dpi)

    # DOS fill
    ax.fill_between(global_element_dictionary['Total DOS']['energy'], global_element_dictionary['Total DOS']['dos'], color = fill_color, alpha = 0.2, label = 'Total DOS')#, figure = element_name)
    if show_fermi_level == True:
        plt.vlines(x= 0, ymin= 0, ymax= fermi_level_max_height, colors= fermi_level_color, linestyles= fermi_level_line_style, label= "Fermi Level")

    # labels
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)


    # general tick parameters
    ax.tick_params(direction = tick_direction, top = top_ticks, bottom = bottom_ticks, left = left_ticks, right = right_ticks)
    ax.yaxis.set_major_locator(tkr.MultipleLocator(y_major_tick_multiple))
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

    # x ticks
    # TODO

    # y ticks
    # TODO

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
    orbital_keys = ['energy', 's1', 'p1', 'p2', 'p3', 'd1', 'd2', 'd3', 'd4', 'd5', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7']
    for key in orbital_keys:
        orbital_dictionary[key] = []

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
        # makes a unique element entry based on the number after the element
        # i.e. CsPbBr3 would return Cs, Pb, Br1, Br2, Br3
        elif char.isnumeric():
            i = 1
            temp_recursive_element = ""
            while i <= int(char):
                temp_recursive_element = temp_element + str(i)
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
                for orbital_label in ['energy', 's1', 'p1', 'p2', 'p3', 'd1', 'd2', 'd3', 'd4', 'd5', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7']:
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

    return global_element_dictionary   

def duplicate_element_check(element_dictionary):
    # declare and initialize our variables
    combined_elements_parent_array = []
    combined_elements_child_array = []
    element_current = ''
    element_buffer = ''
    element_tracker = ''
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
                        if element_current != '' and combined_elements_child_array != []:
                            combined_elements_parent_array.append(combined_elements_child_array)

                        # reset child array
                        combined_elements_child_array = []

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
                        combined_elements_child_array.append(last_element)
                        combined_elements_child_array.append(element)
                        first_iteration_per_element = False

                    else:
                        combined_elements_child_array.append(element)

                    last_element = element

        # remember the last element to assign later if needed
        last_element = element

    # catches if the last element is a duplicate
    if duplicate_element == True:
        combined_elements_parent_array.append(combined_elements_child_array)

    return combined_elements_parent_array

def graph_by_suborbital(element_dictionary):
        if element_dictionary == None:
            element_dictionary = global_element_dictionary
    
        for element in element_dictionary:
            # total DOS is filled between seperately 
            if element == "Total DOS":
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



                        match orbital:
                            case 's1':
                                label = element + ' s'
                            case 'p1':
                                label = element + ' p(y)'
                            case 'p2':
                                label = element + ' p(z)'
                            case 'p3':
                                label = element + ' p(x)'
                            case 'd1':
                                label = element + ' d(x^2 - y^2)'
                            case 'd2':
                                label = element + ' d(yz)'
                            case 'd3':
                                label = element + ' d(z^2)'
                            case 'd4':
                                label = element + ' d(xz)'
                            case 'd5':
                                label = element + ' d(xy)'
                            case 'f1':
                                label = element + ' f(y(3x^2 - y^2))'
                            case 'f2':
                                label = element + ' f(z(x^2 - y^2))'                                                                                                
                            case 'f3':
                                label = element + ' f(yz^2)'
                            case 'f4':
                                label = element + ' f(z^3)'
                            case 'f5':
                                label = element + ' f(xz^2)'
                            case 'f6':
                                label = element + ' f(xyz)'
                            case 'f7':
                                label = element + ' f(x(x^2 - 3y^2))'



                        plt.plot(temp_x, temp_y, label = label)
                        plt.legend() 
                        ax.legend(ncols = 3)

                    except IndexError and ValueError:
                        pass

            save_figure_check(element_figure)

def graph_by_orbital(element_dictionary):
    if element_dictionary == None:
        element_dictionary = global_element_dictionary
    
    for element in element_dictionary:
        try:
            # 'Total DOS' is handled seperately
            if element == 'Total DOS':
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
                    plt.plot(temp_orbital_sum_dictionary['energy'],temp_orbital_sum_dictionary[shell], label = element + " " + shell, figure = element_figure)
                    ax.legend()

                except ValueError as error:
                    print("No orbital at", element, shell)

                plt.legend()

            # plt.show()
            save_figure_check(element_figure)

        except TypeError as error:
                print(error)

def graph_by_element(element_dictionary):
    if element_dictionary == None:
        element_dictionary = global_element_dictionary

    # iniitalize graph settings
    if dark_mode == True:
        plt.style.use('dark_background')

    element_figure, ax = initialize_graph_settings()
    line_style
    # submit one element at a time
    for element in element_dictionary:    
        try:
            #TODO: REMOVE REDUNDANT TRY CATCH BLOCK
            # call the graphing function
            if element == 'Total DOS':
                continue

            temp_element_sum_array = element_sums(element_dictionary[element])
            # call the figure we created settings for
            # figure size
            plt.plot(element_dictionary['Total DOS']['energy'], temp_element_sum_array, label = element, figure = element_figure)
            ax.legend()

        except TypeError as error:
            print(error)

    save_figure_check(element_figure)
    # plt.show()

#SUBMIT ONE ELEMENT AT A TIME
def orbital_shell_sums(orbital_dictionary):
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

    #TODO: call shell sums here and total them
    temp_element_sums = []
    temp_shell_sums = orbital_shell_sums(orbital_dictionary)
    for i in range(len(orbital_dictionary['energy'])):
        try:
            # try them one at a time
            energy = list(temp_shell_sums['energy'])
            temp_element_sums.append(0)
            temp_element_sums[i] += temp_shell_sums['s'][i] 
            temp_element_sums[i] += temp_shell_sums['p'][i] 
            temp_element_sums[i] += temp_shell_sums['d'][i] 
            temp_element_sums[i] += temp_shell_sums['f'][i] 

        except (ValueError, IndexError) as error:
            print("No shell found at", error)
            pass

    return temp_element_sums


if __name__ == "__main__":

    try:
        element_dictionary = parse_DOS('DOSCAR')

        # graph_by_suborbital(element_dictionary) 
        # graph_by_orbital(element_dictionary)   
        graph_by_element(element_dictionary)

        #debugging
        duplicate_element_check(element_dictionary)
        plt.show()

    except FileNotFoundError:
        print("ERROR: DOSCAR file not found in current folder.")
    