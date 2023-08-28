import comedian
import demographic
import ReaderWriter
import timetable
import random
import math
#global variable to allow us for a mathematical calculation to get the respective day when slotting a demographic, comedian pair into the timetable
days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

##class to store all the demographics, with all the comedians from the initial list which satisfy the demographic and a counter to count 
##how many comedians satisfy the demographic, this is important which is our deciding factor for our MRV heuristic
class Demographic:
	def __init__(self,demographic,comedian_List,tempTable,testOrMain):
		self.demographic = demographic
		temp = comedian_List.copy()
		for comedian in comedian_List:
			if testOrMain is False:
				if all(item in comedian.comedian.themes for item in demographic.topics):
					pass
				else:
					temp.remove(comedian)
			else:
				if any(item in comedian.comedian.themes for item in demographic.topics):
					pass
				else:
					temp.remove(comedian)
		temp.sort(key=lambda x: x.counter)
		self.comList = temp
		self.counter = len(temp)
		self.isTest = testOrMain
	
#to implement LCV for task 1 and 2 we then choose the comedian which has the least matches with other demographics.
class Comedian:

	def __init__(self,comedian,demographic_List,temptable,testOrMain):
		self.comedian = comedian
		i = 0
		for demographic in demographic_List:
			if testOrMain is False:
				if all(item in comedian.themes for item in demographic.topics): 
					i = i + 1
			else:
				if any(item in comedian.themes for item in demographic.topics): 
					i = i + 1
		self.counter = i
	pass


class Scheduler:

	def __init__(self,comedian_List, demographic_List):
		self.comedian_List = comedian_List
		self.demographic_List = demographic_List

	#Using the comedian_List and demographic_List, the this class will create a timetable of slots for each of the 5 weekdays in a week.
	#The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	#	timetableObj.addSession("Monday", 1, comedian_Obj, demographic_Obj, "main")
	#This line will set the session slot '1' on Monday to a main show with comedian_obj, which is being marketed to demographic_obj.
	#Note here that the comedian and demographic are represented by objects, not strings.
	#The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	#The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in Task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in Tasks 2 and 3.
	#Comedian (3rd argument) and Demographic (4th argument) can be assigned any value, but if the comedian or demographic are not in the original lists,
	#	your solution will be marked incorrectly.
	#The final, 5th argument, is the show type. For Task 1, all shows should be "main". For Tasks 2 and 3, you should assign either "main" or "test" as the show type.
	#In Tasks 2 and 3, all shows will either be a 'main' show or a 'test' show

	#demographic_List is a list of Demographic objects. A Demographic object, 'd' has the following attributes:
	# d.reference  - the reference code of the demographic
	# d.topics - a list of strings, describing the topics that the demographic likes to see in their comedy shows e.g. ["Politics", "Family"]

	#comedian_List is a list of Comedian objects. A Comedian object, 'c', has the following attributes:
	# c.name - the name of the Comedian
	# c.themes - a list of strings, describing the themes that the comedian uses in their comedy shows e.g. ["Politics", "Family"]

	#For Task 1:
	#Keep in mind that a comedian can only have their show marketed to a demographic
	#	if the comedian's themes contain every topic the demographic likes to see in their comedy shows.
	#Furthermore, a comedian can only perform one main show a day, and a maximum of two main shows over the course of the week.
	#There will always be 25 demographics, one for each slot in the week, but the number of comedians will vary.
	#In some problems, demographics will have 2 topics and in others 3 topics.
	#A comedian will have between 3-8 different themes.

	#For Tasks 2 and 3:
	#A comedian can only have their test show marketed to a demographic if the comedian's themes contain at least one topic
	#	that the demographic likes to see in their comedy shows.
	#Comedians can only manage 4 hours of stage time a week, where main shows are 2 hours and test shows are 1 hour.
	#A Comedian cannot be on stage for more than 2 hours a day.

	#You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need.
	#Furthermore, you should not import anything else beyond what has been imported above.
	#To reiterate, the five calls are timetableObj.addSession, d.reference, d.topics, c.name, c.themes

	#this is a function, recursively called which handles all our backtracking for task 1
	def recursive_backtracking(self,timetableObj,counter,comedian_count,dayslist,demoList):
		#terminates once the timetable is filled out
		if counter == 25:
			return True
		#iterates through the demographics in order of, the least amount of comedians possible to be allocated to it, this is our MRV heuristic
		for demo in demoList:
			#iterates through the comedians in the order of which comedian is least applicable to the most, representing our LCV heruistic
			for comedian in demo.comList:
				##first check if the comedian already performs in the day
				if comedian.comedian.name in dayslist[counter//5]:
					dayCheck = False
				else:
					dayCheck = True
				##now check if the comedian performs too many times in the week, i.e. more than twice
				appearances = comedian_count.get(comedian.comedian.name, 0)

				##now check if the comedian matches the demographic and combine with previous checks 
				if all(item in comedian.comedian.themes for item in demo.demographic.topics) and appearances < 2 and dayCheck:
					##if it can be added add it
					timetableObj.addSession(days[counter//5] , (counter % 5) + 1, comedian.comedian, demo.demographic, "main")
					##update our array and dictionary
					dayslist[counter//5].append(comedian.comedian.name)
					if comedian.comedian.name in comedian_count:
						comedian_count[comedian.comedian.name] = comedian_count[comedian.comedian.name] + 1
					else:
						comedian_count[comedian.comedian.name] = 1
					# Recursively search for a solution with the updated assignment
					newArray = demoList.copy()
					newArray.remove(demo)
					result = self.recursive_backtracking(timetableObj, counter + 1,comedian_count,dayslist,newArray)
					if result is not None:
						return result

					# Remove the assignment and try the next value
					dayslist[counter//5].pop()
					comedian_count[comedian.comedian.name] = comedian_count[comedian.comedian.name] - 1
		return None
	"""
	Task 1 Preamble:
	the problem we are presented with a is Constraint Satisfaction Problem (CSP) and a Search Problem. This led me to 
	choose a backtracking solution as my method to solving this problem:
	My solution iterates through the demographics then all the comedians per demographic to find a fit for the specified 
	timeslot the algorithm is currently on.
	My algorithm utilises MRV (Minimum Remaining Value) and LCV (Lowest Constraining Variable) heuristics as follows:
	the demographics are iterated in the order of least amount of comedians that can be assigned to it i.e. if demo1 has 3 possible valid comedians
	and demo2 has 4 then demo1 is considered before demo2.
	LCV is implemented via the comedians, the comedian which has the least amount of different demographics which it can perform in  
	is considered before comedians that can perform in more demographics.
	Reasoning:
	My reasoning behind choosing backtracking to be the method of choice is due to the following reasons:
	- the problem is both a search problem and a CSP, in these problems backtracking particularly thrives in 
	- additionally there are usually many solutions because the len(comedian_List) >= len(demographic_List) so backtracking is suited to this problem
	"""
	def createSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(1)

		#Here is where you schedule your timetable

		#here we need to establish our stores 
		demoList = [] #to hold a full list of our demographics represented as the new Demographic object 
		comeList = [] #to hold a full list of our comedians represented as the new Comedian object
		#create our Comedian objects
		for comedian in self.comedian_List:
			temp = Comedian(comedian,self.demographic_List,timetableObj,False)
			comeList.append(temp)
		#create our demographic objects
		for demographic in self.demographic_List:
			temp = Demographic(demographic,comeList,timetableObj,False)
			demoList.append(temp)
		#sort the demographics by minimum remaining variables: least amount of comedians that can be applied to a demographic to most
		demoList.sort(key=lambda x: x.counter)
		#instantiate our stores for keeping track of the comedians that perform each day and the amount of hours total in the week
		dayslist = [[] for _ in range(5)] 
		comedian_count = dict()
		#begin our backtracking function
		result = self.recursive_backtracking(timetableObj, 0,comedian_count,dayslist,demoList)
		if result is None:
			return None
		else:
			return timetableObj

	#Now, for Task 2 we introduce test shows. Each day now has ten sessions, and we want to allocate one main show and one test show
	#	to each demographic.
	#All slots must be either a main or a test show, and each show requires a comedian and a demographic.
	#A comedian can have their test show marketed to a demographic if the comedian's themes include at least one topic the demographic likes.
	#We are also concerned with stage hours. A comedian can be on stage for a maximum of four hours a week.
	#Main shows are 2 hours long, test shows are 1 hour long.
	#A comedian cannot be on stage for more than 2 hours a day.

	#this is a function, recursively called which handles all our backtracking for task 2
	def recursive_backtrackingTask2(self,timetableObj,counter,comedian_count,dayslist,demoList):
		#terminates once the timetable is filled out
		if counter == 50:
			return True
		#iterates through the demographics in order of, the least amount of comedians possible to be allocated to it, this is our MRV heuristic
		#this includes both the test and main instance of a demographic
		for demo in demoList:
			#iterates through the comedians in the order of which comedian is least applicable to the most, representing our LCV heruistic
			for comedian in demo.comList:
				##first check if the comedian already performs too much in the day
				if demo.isTest == False:
					if dayslist[counter//10].count(comedian.comedian.name) > 0:
						dayCheck = False
					else:
						dayCheck = True
				else:
					if dayslist[counter//10].count(comedian.comedian.name) > 1:
						dayCheck = False
					else:
						dayCheck = True
				##now check if the comedian performs too many times in the week, i.e. more than twice
				if demo.isTest == False:
					if comedian_count.get(comedian.comedian.name, 0) > 2:
						appearanceCheck = False
					else:
						appearanceCheck = True
				else:
					if comedian_count.get(comedian.comedian.name, 0) > 3:
						appearanceCheck = False
					else:
						appearanceCheck = True

				##combine the checks (note:we dont need to check if the comedian matches the demographic as this is already ensured as we only iterate through comedians which
				# are able to be assigned to the demographic)
				if appearanceCheck and dayCheck:
					##if it can be added add it
					##test and main affect our stores differently so must be handled seperately
					if demo.isTest == False:
						timetableObj.addSession(days[counter//10] , (counter % 10) + 1, comedian.comedian, demo.demographic, "main")
						#add the comedian to our dayslist twice , to represent per hour performed
						dayslist[counter//10].append(comedian.comedian.name)
						dayslist[counter//10].append(comedian.comedian.name)
						if comedian.comedian.name in comedian_count:
							comedian_count[comedian.comedian.name] = comedian_count[comedian.comedian.name] + 2
						else:
							comedian_count[comedian.comedian.name] = 2
						newArray = demoList.copy()
						newArray.remove(demo)
						result = self.recursive_backtrackingTask2(timetableObj, counter + 1,comedian_count,dayslist,newArray)
						if result is not None:
							return result

						# Remove the assignment and try the next value
						dayslist[counter//10].pop()
						dayslist[counter//10].pop()
						comedian_count[comedian.comedian.name] = comedian_count[comedian.comedian.name] - 2
					else:
						timetableObj.addSession(days[counter//10] , (counter % 10) + 1, comedian.comedian, demo.demographic, "test")
						dayslist[counter//10].append(comedian.comedian.name)
						if comedian.comedian.name in comedian_count:
							comedian_count[comedian.comedian.name] = comedian_count[comedian.comedian.name] + 1
						else:
							comedian_count[comedian.comedian.name] = 1
						newArray = demoList.copy()
						newArray.remove(demo)
						result = self.recursive_backtrackingTask2(timetableObj, counter + 1,comedian_count,dayslist,newArray)
						if result is not None:
							return result

						# Remove the assignment and try the next value
						dayslist[counter//10].pop()
						comedian_count[comedian.comedian.name] = comedian_count[comedian.comedian.name] - 1
		return None
	"""
	Task 2 Preamble:
	The problem we are presented is another CSP + search problem, leading me to chose backtracking again.
	My solution is almost a replica of my task1 solution, differences being in the validation
	In this problem our search space is vastly expanded, making backtracking somewhat unfavourable, however with the implementation
	of MRV and LCV this becomes much less problematic
	The nature of our MRV heuristic commonly gathers all the main shows first and then all the test shows.
	This is significant as instead of vastly expanding the search space we are doing 2 seperate CSP problems, this is true due to the following:
	with our demographics we only append the comedians which completely satisfy the demographic, thus the ordering will mean that test shows
	will most likely NOT be given a comediant which is needed for a main show. We could also conclude that if a backtracking were to occur, itd be in the main portion
	or the Test portion, and rarely crossover.
	This henceforth makes backtracking still favourable for the same reasons as presented in the preamble of Task 1.
	The other additional constraints do not affect our backtracking much as they replace the constraints in Task 1
	"""
	def createTestShowSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(2)

		#this is the same as task 2 but we add another iteration where we make comedian and demographic objects with "test" as its showType 
		demoList = []
		comeList = []
		for comedian in self.comedian_List:
			temp = Comedian(comedian,self.demographic_List,timetableObj,False)
			comeList.append(temp)
			temp = Comedian(comedian,self.demographic_List,timetableObj,True)
			comeList.append(temp)
		for demographic in self.demographic_List:
			temp = Demographic(demographic,comeList,timetableObj,False)
			demoList.append(temp)
			temp = Demographic(demographic,comeList,timetableObj,True)
			demoList.append(temp)
		demoList.sort(key=lambda x: x.counter)
		dayslist = [[] for _ in range(5)]
		comedian_count = dict()
		result = self.recursive_backtrackingTask2(timetableObj, 0,comedian_count,dayslist,demoList)
		if result is None:
			return None
		else:
			return timetableObj

	#Now, in Task 3 it costs £500 to hire a comedian for a single main show.
	#If we hire a comedian for a second show, it only costs £300. (meaning 2 shows cost £800 compared to £1000)
	#If those two shows are run on consecutive days, the second show only costs £100. (meaning 2 shows cost £600 compared to £1000)

	#It costs £250 to hire a comedian for a test show, and then £50 less for each extra test show (i.e., £200, £150 and £100)
	#If a test shows occur on the same day as anything else a comedian is in, then its cost is halved.

	#Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
	#You are not expected to always find the optimal solution, but you should be as close as possible.
	#You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here.
	"""
	Task 3 Preamble:
	My method Chosen was Simulated Annealing to decrease the cost. I will evaluate why i chose this algorithm with respect 
	to other methods:
	-A* algorithm -> the search space is far to large for A* to be effective, if A* is to be used we would need to cull
					branches, thus possibly resulting in a suboptimal solution
	-hill climbing/gradient descent -> this is susceptible to being stuck in local minima, while this is a good choice due to the low computational complexity and 
										ease of implementation, simulated annealing is far more likely to reach a global minimal value without much trade off on runtime 

	-genetic algorithm -> the computational time is much larger to produce a similar result to what simulated annealing might. This is due to the following reasons:
						- we have to generate a minimal cost solution + a valid solution whereas in SA we already have a valid solution 
						- the fitness function would need to be calculated for every element in the population, consider a population of 1000 with 100 generations:
						- we would calculate this 100000 times, despite having a relatively low population size with respect to the total amount of possible assignments
						- due to strict constraints there isn't a clear way to gague how "good" a solution is, we would need a method to differentiate, which hard constraints are softer than others, whilst balancing the cost and a reward for "good" traits
						- it is not scalable, if the comedian list doubled in value, the parameters fine-tuned to solve the previous problem would not generate an optimal solution with the new problem, if it even generates a valid timetable.
						wheras in SA we are very likely to obtain a solution with a lower cost than that of the same solution passed into task 2.

	In a SA algorithm the temperature must be carefully selected as it can have drastic effects on the optimality of the solutions:
	i decided to use a linear cooling function, which results in the temperature to decrease as the iteration amount increases, i believe my initial value of temperature allows the 
	search space to be explored efficiently and the function is chosen as it can run in O(1) time complexity, as a result the average of my solution through testing
	results in timetables of 10050 (global optimum) ~ 10250 with occasional spikes in the 10600 range.
	My simulated annealing algorithm is as follows:
	SIMULATED ANNEALING:
			Write cost function to figure out the cost of the timetable
			implement a random neighbour function:
				consists of:
				- randomly select a timeslot and change the comedian to a valid comedian
				- swap it with another timeslot
			
			if it is a lower cost accept 
			it and continue, else if adoption function returns true accept it otherwise
			reject it and continue
			run for a certain amount of iterations
	"""

	def createMinCostSchedule(self):
		#Do not change this line
		"""populate our demographic dictionary with the respective demographic name -> show type -> demographic obj
			this is stored as a dict(dict(Demographic)) this is useful to obtain a valid marketable comedian easily for any demographic, showtype pair"""
		timetableObj = timetable.Timetable(3)
		demoDict = dict()
		for demographic in self.demographic_List:
			demoDict[demographic.reference] = dict()
			demoDict[demographic.reference]["main"] = []
			demoDict[demographic.reference]["test"] = []
			for comedian in self.comedian_List:
				if any(item in comedian.themes for item in demographic.topics):
					demoDict[demographic.reference]["test"].append(comedian)
				if all(item in comedian.themes for item in demographic.topics):
					demoDict[demographic.reference]["main"].append(comedian)
		"""obtain our task 2 solution to begin with a valid solution"""
		goodTT = self.createTestShowSchedule()
		"""our 'best' variable keeps track of the cheapest valid timetable throughout our SA (simulated annealing) algorithm"""
		best = goodTT
		bestCost = self.findCost(goodTT,self.comedian_List,self.demographic_List)
		numOfiterations = 11000 #the number of iterations we run SA for 
		for i in range(numOfiterations):
			"""try make neighbour"""
			while True:
				try:
					neighbour = self.makeNeighbour(goodTT,demoDict)
					break
				except ValueError:
					continue
			"""if a valid neighbour is made we need to now obtain its cost"""
			neighbourCost = self.findCost(neighbour, self.comedian_List, self.demographic_List)
			ogCost = self.findCost(goodTT, self.comedian_List, self.demographic_List)
			""" if the neighbour has a lower cost than our previous state then we accept it, we also check if it is better than our current
				best timetable """
			if neighbourCost < ogCost:
				if neighbourCost < bestCost:
					best = neighbour
					bestCost = neighbourCost
				goodTT = neighbour
			else:
				"""if the neighbour has a worse cost than the current timetable we have we execute our adoption function"""
				if self.adoption(neighbourCost,ogCost,i, numOfiterations):
					goodTT = neighbour
				else:
					pass
		return best
		#Here is where you schedule your timetable
		##
		
		
	def makeNeighbour(self,timetableObj, demoDict):
		days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

		"""here we randomly select a timeslot to mutate then we swap this with another randomly selected timeslot"""
		slotToChange = random.randint(0,49)
		slotToSwap   = random.randint(0,49)
		"""obtain the slots"""
		slot1 = timetableObj.schedule[days[slotToChange//10]][(slotToChange % 10) + 1] ##the slot to mutate
		slot2 = timetableObj.schedule[days[slotToSwap//10]][(slotToSwap % 10) + 1] ##the slot to swap with the mutated

		"""now mutate the comedian"""

		newSlot = [random.choice(demoDict[slot1[1].reference][slot1[2]]),slot1[1], slot1[2]] ##mutated slot

		"""now we construct the timetable if it is valid
		    as we know the rest of the time table is already valid, since they dont change we just need to check
			the values we have changed are valid, this consists of:
			- 4hr performance per week (for just the mutated value)
			- 2hr performance per day (for both moving values)
		"""
		neighbour = timetable.Timetable(3)
		dayslist = [[] for _ in range(5)]
		comedian_count = dict()
		addedComedian = None
		slotType = None
		for i in range(50):
			"""construct the timetable"""
			if i == slotToChange:
				addedComedian = slot2[0].name
				slotType = slot2[2]
				neighbour.addSession(days[i//10],(i % 10) + 1 ,slot2[0], slot2[1], slot2[2])
			elif i == slotToSwap:
				addedComedian = newSlot[0].name
				slotType = newSlot[2]
				neighbour.addSession(days[i//10],(i % 10) + 1 ,newSlot[0], newSlot[1], newSlot[2])
			else:
				one = timetableObj.schedule[days[i//10]][(i % 10) + 1][0]
				addedComedian = one.name
				two = timetableObj.schedule[days[i//10]][(i % 10) + 1][1]
				three = timetableObj.schedule[days[i//10]][(i % 10) + 1][2]
				slotType = three
				neighbour.addSession(days[i//10],(i % 10) + 1 ,one, two ,three)
			"""after every addition to the timetable check if its valid, if not we can stop creating this neighbor and attempt to make another"""
			if slotType == "main":
				if addedComedian in comedian_count:
					comedian_count[addedComedian] = comedian_count[addedComedian] + 2
				else:
					comedian_count[addedComedian] = 2
				dayslist[i//10].append(addedComedian)
				dayslist[i//10].append(addedComedian)
			else:
				if addedComedian in comedian_count:
					comedian_count[addedComedian] = comedian_count[addedComedian] + 1
				else:
					comedian_count[addedComedian] = 1
				dayslist[i//10].append(addedComedian)
			if dayslist[i//10].count(addedComedian) > 2:
				raise ValueError
			elif comedian_count.get(addedComedian, 0) > 4:
				raise ValueError
			else:
				continue
		return neighbour 

	"""cost function to find the cost of a given timetable"""
	def findCost(self,timetableObj,comedian_List, demographic_List):

		"""establish our stores"""
		comedian_Count = dict()
		schedule_Cost = 0
		comedians_Yesterday = list()
		main_show_Count = dict()
		test_show_Count = dict()

		"""add all comedians to the stores so we don't need to check if they already exist as we know they do"""
		for comedian in comedian_List:
			main_show_Count[comedian.name] = 0
			test_show_Count[comedian.name] = 0
			comedian_Count[comedian.name] = 0

		"""iterate through every day of the timetable"""
		for day in timetableObj.schedule:
			day_List = timetableObj.schedule[day]

			comedians_Today = dict()
			possible_Discount = dict()

			for entry in timetableObj.schedule[day]:
				[comedian, demographic, show_type] = day_List[entry]
				if comedian.name in comedians_Today:
					#This branch means the comedian is already on stage today.
					
					#We calculate the cost for the show, if it is a main show.
					if show_type == "main":
						comedians_Today[comedian.name] = comedians_Today[comedian.name] + 2
						main_show_Count[comedian.name] = main_show_Count[comedian.name] + 1
						if main_show_Count[comedian.name] == 1:
							schedule_Cost = schedule_Cost + 500
						elif comedian.name in comedians_Yesterday:
							schedule_Cost = schedule_Cost + 100
						else:
							schedule_Cost = schedule_Cost + 300
					else:
						#We calculate the cost of a test show
						comedians_Today[comedian.name] = comedians_Today[comedian.name] + 1
						test_show_Count[comedian.name] = test_show_Count[comedian.name] + 1
						initial_test_show_Cost = (300 - (50 * test_show_Count[comedian.name])) / 2
						schedule_Cost = schedule_Cost + initial_test_show_Cost

						if comedian.name in possible_Discount:
							schedule_Cost = schedule_Cost - possible_Discount.pop(comedian.name)
				else:
					#This branch means the comedian has not yet been on stage today
					#We calculate the costs correspondingly
					if show_type == "main":
						comedians_Today[comedian.name] = 2
						main_show_Count[comedian.name] = main_show_Count[comedian.name] + 1
						if main_show_Count[comedian.name] == 1:
							schedule_Cost = schedule_Cost + 500
						elif comedian.name in comedians_Yesterday:
							schedule_Cost = schedule_Cost + 100
						else:
							schedule_Cost = schedule_Cost + 300
					else:
						comedians_Today[comedian.name] = 1

						test_show_Count[comedian.name] = test_show_Count[comedian.name] + 1
						initial_test_show_Cost = (300 - (50 * test_show_Count[comedian.name]))
						schedule_Cost = schedule_Cost + initial_test_show_Cost
						possible_Discount[comedian.name] = initial_test_show_Cost / 2


			comedians_Yesterday = comedians_Today

		"""we assign the cost and return the cost"""
		timetableObj.cost = schedule_Cost
		return schedule_Cost

	"""our adoption function to decide if we accept the worse neighbor or not"""
	def adoption(self,newCost, oldCost, iteration, maxiteration):
		"""calculate the change in cost"""
		deltaE = newCost - oldCost
		"""calculate our temperature based on our linear formula """
		temperature = (1 - (iteration)/ maxiteration) * 20
		tester = math.exp(-1 * ((deltaE)/(temperature ) + 1))
		if tester > random.uniform(0,1): 
			return True
		else:
			return False



