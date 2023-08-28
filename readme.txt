There are six files, as follows:

scheduler.py - This contains 3 crucial methods, namely createSchedule, createTestShowSchedule and createMinCostSchedule. The first one must return a valid Timetable object for Task 1, with each day and each slot assigned. The second must return a valid timetable for the Task 2, which consists of ten sessions a day, with main and test shows. The third method must return a legal schedule for Task 3, which also has the lowest cost possible. 

runScheduler.py - This is the file that is run to test your solution. This file will run your scheduler, test whether it creates a legal schedule and print out the cost. Feel free to edit line 21 to load in a different problem file, and edit the scheduler method called from createSchedule to createTestShowSession or createMinCostSchedule.

There are four other files. They have the following functions:

comedian.py - Contains the comedian class. Notably, a comedian is defined as a name and a list of themes. While this class has a few mutator methods (setName, setThemes, addTheme), the only legal ways for you to use these classes in this coursework are as follows:
	c.name -- Returns the name of comedian c as a string.
	c.themes -- Returns the themes used by comedian c as a list of strings.

demographic.py - Contains the demographic class. Notably, a demographic is defined as a reference code and a list of topics. While this class has a few mutator methods (setReference, setTopics, addTopic), the only legal ways for you to use this class in the coursework are as follows:
	d.reference -- Returns the reference code of demographic d as a string.
	d.topics -- Returns the topics that appeal to demographic d as a list of strings.

timetable.py - Contains the Timetable class. This class will be used to store the schedule you create, and a show slot can be assigned a demographic and a comedian through the 'addSession' method, as described in the preamble for schedule.py. Importantly, the only valid days of the week are Monday, Tuesday, Wednesday, Thursday and Friday and the only slot numbers that are valid are 1, 2, 3, 4, 5, 6 ,7 , 8, 9 and 10. This class also contains the method to allow you to check that your schedule is legal, which is used in runScheduler.py. However, this method *cannot* be used by your submitted solution in the scheduler.py file. When a timetable is created, the task number is also given, so that it can check against the correct rules. The following method can be used in your final submission:

	timetable.addSession(day, timeslot, comedian, demographic, show_Type) -- This will fill the designated timeslot (which should be a number) on the given day (Monday, Tuesday, Wednesday, Thursday, or Friday) with the given comedian and demographic. show_Type should be a string with the value of either 'main' or 'test'. For Task 1 all sessions should be 'main' and for Tasks 2 and 3 there will be both 'main' and 'test' sessions.

ReaderWriter - Class for reading in the example problems, and is also capable of writing out lists of comedians and demographics if you wish to create more problems to test your solution against. The use of the reader method can be seen in runSchedule.py. To use the writer method it must be passed a list of comedian objects, a list of demographic objects and a filename. The readRequirements method converts the text file it is passed into a list of comedian and demographic objects.





