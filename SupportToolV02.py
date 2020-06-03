from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import PySimpleGUI as sg
import time

# These are the default messages send to the people. Every problem has their own part with appropraite context.
def message(name, charactername, problems):
	message = ''
	message1 = f'Hey {name},\n\nThe staff team have looked over your character {charactername}.\nWe have found a few problems with your character.\n\n'
	message2 = 'If these changes have not been made within 24 hours, then you will be temporarily banned from the DayZRP server.\nIf you think your character does feel realistic, feel free to PM back and explain why.'
	messages = []
	for problem in problems:
		if problem == 'Date of birth':
			message3 = 'The current Date of birth would mean your character was born this week.\nWe do not allowe this and you would have to change this to a realistic Date of birth.\n\n'
			messages.append(message3)
		if problem == 'Picture':
			message4 = 'The Picture must represent your character.\nIt can only be a screenshot of your ingame character, or a real picture (from yourself or google).\nYou can however have other pictures as the second and third picture.\nYou would have to change your first picture to follow our guidelines.\n\n'
			messages.append(message4)
		if problem == 'Weight':
			message5 = 'The current weight does not meet our guidelines.\nThe weight of your character has to be somewhere between 50 and 150 kg.\nKeep in mind that kg is twice as much as pounds.\n\n'
			messages.append(message5)
		if problem == 'Height':
			message6 = 'The current height does not meet our guidelines.\nThe height of your character has to be somewhere between 150 and 200 cm.\n\n'
			messages.append(message6)
		if problem == 'Name':
			message7 = 'Your current character name does not meet our guidelines.\nThe name of your character should only be a first and last name.\nYou cannot use prefixes and all uppercase letters.\nThe only way to fix your character name is to delete your character and make a new one.\n\n'
			messages.append(message7)
	if len(problems) == 1:
		message = f'{message1}{messages[0]}{message2}'
	if len(problems) == 2:
		message = f'{message1}{messages[0]}Also,\n\n{messages[1]}{message2}'
	if len(problems) == 3:
		message = f'{message1}{messages[0]}Also,\n\n{messages[1]}Also,\n\n{messages[2]}{message2}'
	if len(problems) == 4:
		message = f'{message1}{messages[0]}Also,\n\n{messages[1]}Also,\n\n{messages[2]}Also,\n\n{messages[3]}{message2}'
	if len(problems) == 5:
		message = f'{message1}{messages[0]}Also,\n\n{messages[1]}Also,\n\n{messages[2]}Also,\n\n{messages[3]}Also,\n\n{messages[4]}{message2}'
	return message

#Setup list
list_of_links = []

#Create browser
driver = webdriver.Chrome()
sg.change_look_and_feel('SystemDefault')

#Login part
driver.get("https://www.dayzrp.com/login/")
layout = [[sg.Text('Have you logged in? Click OK to continue.', justification='left')], [sg.Ok()]]
window = sg.Window('Are you ready?', layout)
event, values = window.read()
window.close()

#Go to character list and collect them
driver.get("https://www.dayzrp.com/charactersmod/")
table_id = driver.find_element_by_css_selector('table.ipsTable.ipsTable_responsive.ipsTable_zebra')
tbody = table_id.find_element_by_tag_name('tbody')
containers = tbody.find_elements_by_tag_name('tr')
for container in containers:
	col = container.find_elements_by_tag_name('td')[1]
	item = col.find_elements_by_tag_name('a')
	list_of_links.append((item[0].get_attribute('href'),col.text))
	
#Select last checked
value = []
for i in list_of_links:
	value.append(i[1])
layout = [[sg.Listbox(values=value, size=(30, 50))],[sg.Button('Select')]]
window = sg.Window('Select last checked person.', layout)
event, values = window.read()
window.close()
need_checking = []
for name in list_of_links:
	if name[1] == values[0][0]:
		break
	else:
		need_checking.append(name)
list_of_profiles = {}

#Start checking
for profile in need_checking:
	info = []
	i = 0
	driver.get(profile[0])
#Check if the person is whitelisted or not
	driver.find_element_by_class_name('ipsType_break').click()
	whitelist = driver.find_elements_by_class_name('ipsDataItem_generic')
#Skip person if he is not whitelisted
	if whitelist[1].text == "NO":
		continue;
	driver.get(profile[0])
#Give popup to see what is good and what is wrong
	layout = [
	[sg.Text('Is the first picture correct?', justification='left')],
	[sg.Checkbox('Yes', size=(12, 1)), sg.Checkbox('No', size=(12, 1))],
	[sg.Text('Is the name correct?', justification='left')],
	[sg.Checkbox('Yes', size=(12, 1)), sg.Checkbox('No', size=(12, 1))],
	[sg.Text('Is the backstory correct?', justification='left')],
	[sg.Checkbox('Yes', size=(12, 1)), sg.Checkbox('No', size=(12, 1)), sg.Checkbox('WIP', size=(12, 1))],
	[sg.Ok()]]
	window = sg.Window('Check Page', layout)
	event, values = window.read()
	window.close()
	if values[0] == True:
		picturegood = 'yes'
	if values[1] == True:
		picturegood = 'no'
	if values[2] == True:
		namegood = 'yes'
	if values[3] == True:
		namegood = 'no'
	if values[4] == True:
		backstorygood = 'yes'
	if values[5] == True:
		backstorygood = 'no'
	if values[6] == True:
		backstorygood = 'wip'
#Automatically check heigth, date of birth and weight
	description = driver.find_elements_by_class_name('ipsDataItem_main')
	characterinfo = driver.find_elements_by_class_name('ipsDataItem_generic')
	title = driver.find_elements_by_class_name('ipsType_pageTitle')[0].text
	j = 0
	while j < len(characterinfo):
		texto = (characterinfo[j].text, description[j].text)
		if texto[0] == 'Date of birth':
			if len(texto[1]) == 10:
				i = 1
				info.append(texto)
		if texto[0] == 'Weight':
			if int(texto[1][0:len(texto[1])-3]) < 50 or int(texto[1][0:len(texto[1])-3]) > 150:
				i = 1
				info.append(texto)
		if texto[0] == 'Height':
			if int(texto[1][0:len(texto[1])-3]) < 150 or int(texto[1][0:len(texto[1])-3]) > 200:
				i = 1
				info.append(texto)
		j = j+1
	if namegood == 'no':
		info.append(('Name', 'no'))
		i = 1
	if picturegood == 'no':
		info.append(('Picture', 'no'))
		i = 1
	if backstorygood == 'wip':
		info.append(('Backstory', 'wip'))
		i = 1
	elif backstorygood == 'no':
		info.append(('Backstory', 'no'))
		i = 1
	print('\n')
	if i == 0:
		continue
#Collect everything in a list for message
	else:
		profile_name = driver.find_element_by_class_name('ipsType_break').text
		driver.find_element_by_class_name('ipsType_break').click()
		profile_link = driver.current_url
		profile_id = driver.find_element_by_tag_name('body').get_attribute("data-pageid")
		info.append(('profile_link', profile_link))
		info.append(('character_link', profile[0]))
		info.append(('profile_name', profile_name))
		info.append(('profile_id', int(profile_id)))
		list_of_profiles.update({title:info})
leftovers = []
#Clear invalid CP list txt
open('InvalidCPList.txt', 'w').close()
bericht = ''
#Start creation message
for everyone,reasons in list_of_profiles.items():
	character_name = everyone
	problems = []
	for reason in reasons:
		wip = 'no'
		if reason[0] == 'profile_name':
			name = reason[1]
		if reason[0] == 'profile_id':
			id = reason[1]
		if reason[0] == 'character_link':
			clink = reason[1]
		if reason[0] == 'profile_link':
			link = reason[1]
		if reason[0] == 'Date of birth':
			problems.append('Date of birth')
		if reason[0] == 'Picture':
			problems.append('Picture')
		if reason[0] == 'Height':
			problems.append('Height')
		if reason[0] == 'Weight':
			problems.append('Weight')
		if reason[0] == 'Backstory':
			if reason[1] == 'yes':
				continue
			elif reason[1] == 'wip':
				problems.append('WIP')
			else:
				problems.append('Backstory')
		if reason[0] == 'Name':
			problems.append('Name')
	f = open("InvalidCPList.txt", "a")
	problemen = ' + '.join(problems)
	f.write(f'{character_name} - {clink} - {problemen} - {link}\n')
	bericht += f"{problemen}\n{character_name} {clink} - PM'ed\n"
	f.close()
#Make and send the message
	if not 'Backstory' in problems and not 'WIP' in problems:
		themessage = message(name, character_name, problems)
		driver.get(f"https://www.dayzrp.com/messenger/compose/?to={id}")
		driver.find_element_by_name("messenger_title").send_keys("Incorrect CP")
		time.sleep(2)
		name = driver.find_element_by_class_name('cToken').text
		driver.find_element_by_css_selector('div.cke_wysiwyg_div.cke_reset.cke_enable_context_menu.cke_editable.cke_editable_themed.cke_contents_ltr').send_keys(themessage)
		#Add .click()
		driver.find_element_by_css_selector('button.ipsButton.ipsButton_primary').click()
		time.sleep(2)
#If it was a wip then dont message else add it to a list you still need to message
	else:
		if not 'WIP' in problems:
			leftovers.append(name)
			driver.get(f"https://www.dayzrp.com/messenger/compose/?to={id}")
			driver.find_element_by_name("messenger_title").send_keys("Incorrect CP")
			layout = [[sg.Text('You still have to message: '+ name, justification='left')],[sg.Text('Reasons: ' + problemen)] , [sg.Ok()]]
			window = sg.Window('Do not forget!', layout)
			event, values = window.read()
			window.close()
# Add message to the forums.
driver.get(f"https://www.dayzrp.com/forums/topic/103968-invalid-character-page-pms/#replyForm")
driver.find_element_by_css_selector('div.ipsComposeArea_dummy.ipsJS_show').click()
time.sleep(2)
driver.find_element_by_css_selector('div.cke_wysiwyg_div.cke_reset.cke_enable_context_menu.cke_editable.cke_editable_themed.cke_contents_ltr').send_keys(bericht)
layout = [[sg.Text('Did you finish editing the Invalid Character Page entry?\nBy clicking submit you will automatically submit.', justification='left')], [sg.Submit()]]
window = sg.Window('Finished?', layout)
event, values = window.read()
window.close()
#Add .click()
driver.find_element_by_css_selector('button.ipsButton.ipsButton_primary').click()
time.sleep(1)
driver.close()