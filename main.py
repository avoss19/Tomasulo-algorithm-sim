#!/usr/bin/python

# ECE 474 - Project 1
# Tomasulo's Alg
# By Andrew Voss

# Run: ./main textFile.txt

# input: text file formatted w/ lines:
# 0: number of instructions
# 1: number of cycles
# 2 - EOF: instruction

# Instruction formatting:
# op dest src1 src2

# OP Codes
# 0: add
# 1: sub
# 3: mult
# 4: div

# Reservation stations:
# Add unit: RS1 - RS3
# Mult unit: RS4 - RS5

# Add/Sub - 2 cycles
# Multiply - 10 cycles
# Divide - 40 cycles

# Total of 8 registers
# R0 - R7

# No same-cycle issue and dispatch
# If 2 or more instructions are ready to be dispatched in the same cycle in teh add unit, instruction in lowest reservation has priority
# i.e RS1, RS2, then RS3
# Similarily if two instructions dispatch in the same cycle for multiplication, the lowest reservation has priority
# i.e RS4, then RS5

# Instruction queue can hold up to 10 instructions

import sys

class Instr():
	def __copy__(self):
		return Instr(self.op, self.rst, self.src1, self.src2)

	def copy(self):
		return self.__copy__()

	def __str__(self):
		return str([self.op, self.rst, self.src1, self.src2])

	def __init__(self, op, rst, src1, src2):
		self.op = int(op)
		self.rst = int(rst)
		self.src1 = int(src1)
		self.src2 = int(src2)

		self.state = 0 # 0: issued, 1: dispatch, 2: broadcast
		self.cycles = 0 # cycles in current state

		self.result = None
		
		self.issued = False
		self.dispatched = False
		self.broadcasted = False

	def getCycles(self):
		# Return cycles for OP codes
		# add/sub - 2 cycles
		# mult - 10 cycles
		# div - 40 cycles
		match self.op:
			case 0:
				return 2
			case 1:
				return 2
			case 2:
				return 10
			case 3:
				return 40

	def issue(self, addRes, multRes, rf, rat, cycle, depWait = False):
		# Rewrite
		if(not self.issued):
			if(rat.getReg(self.src1) == None):
				t1 = None
				v1 = rf.getReg(self.src1)
			else:
				t1 = rat.getReg(self.src1)
				v1 = None

			if(rat.getReg(self.src2) == None):
				t2 = None
				v2 = rf.getReg(self.src2)
			else:
				t2 = rat.getReg(self.src2)
				v2 = None

			if(self.op < 2):
				ratRS = addRes.addItem(self.op, t1, t2, v1, v2, cycle)
			else:
				ratRS = multRes.addItem(self.op, t1, t2, v1, v2, cycle)

			rat.setReg(self.rst, ratRS)
			
			self.issued = True
		
		if(not depWait):
			self.state = self.state + 1
			
	def dispatch(self, rf, rat, broadcastWait = False):
		self.cycles = self.cycles + 1
				
		if(not self.dispatched):
			match self.op:
				case 0:
					self.result = rf.getReg(self.src1) + rf.getReg(self.src2)
				case 1:
					self.result = rf.getReg(self.src1) - rf.getReg(self.src2)
				case 2:
					self.result = rf.getReg(self.src1) * rf.getReg(self.src2)
				case 3:
					self.result = rf.getReg(self.src1) / rf.getReg(self.src2)
		
		if(self.getCycles() <= self.cycles and not broadcastWait):
			self.state = self.state + 1

	def broadcast(self, rf):
		if(not self.broadcasted):
			rf.setReg(self.rst, self.result)
		self.broadcasted = True

	def run(self, rf, rat, addReserve, multReserve, cycle, depWait = False, broadcastWait = False):
		match self.state:
			case 0:
				self.issue(addReserve, multReserve, rf, rat, cycle, depWait)
			case 1:
				self.dispatch(rf, rat, broadcastWait)
			case 2:
				self.broadcast(rf)

class InstrQueue():
	# IQ
	def __str__(self):
		instrStr = "Instruction Queue:\n"
		for i in self.instrs:
			match i.op:
				case 0:
					op = "Add"
				case 1:
					op = "Sub"
				case 2:
					op = "Mul"
				case 3:
					op = "Div"
			instrStr = instrStr + "%s, R%d, R%d, R%d\n" % (op, i.rst, i.src1, i.src2)
		return str(instrStr)
	
	def __init__(self, instrs):
		self.pc = 0
		self.instrs = instrs

	def setPC(self, value):
		self.pc = value

	def getPC(self):
		return self.pc

	def execNextInstr(self, rf, rat, addReserve, multReserve, cycle, depWait = False):
		# reset pc counter if all instr are exec
		if(self.pc == len(self.instrs)):
			self.pc = 0
		instr = self.instrs[self.pc].copy()
		self.pc = self.pc + 1

		return instr

class RF():
	def __str__(self):
		return str(self.rf)

	def __init__(self, rf = None, size = 8):
		self.size = size
		if rf != None:
			self.rf = rf
		else:
			self.rf = [None] * size

	def setReg(self, index, value):
		self.rf[index] = value

	def getReg(self, index):
		return self.rf[index]

class RAT(RF):
	def __str__(self):
		s = [("RS%d" % (reg)) for reg in self.rf]
		return str(s)

	def __init__(self, size = 8):
		# RAT initilizes where R0 = RS0, R1 = RS1, ..., RN = RSN
		#super().__init__([i for i in range(0, size)])
		super().__init__([None] * size)

class Reserve():
	def __init__(self, size, rsIndex = 0):
		self.size = size
		self.num = 0 # number of items
		self.rsIndex = rsIndex

		self.op = [None] * size
		self.t1 = [None] * size
		self.t2 = [None] * size
		self.v1 = [None] * size
		self.v2 = [None] * size
		self.busy = [None] * size

	def set(self, op, t1, t2, v1, v2, busy, index):
		self.op[index] = op
		self.t1[index] = t1
		self.t2[index] = t2
		self.v1[index] = v1
		self.v2[index] = v2
		self.busy[index] = busy

	def addItem(self, op, t1, t2, v1, v2, busy):
		index = self.num % self.size

		if(self.num < self.size):
			self.op[self.num] = [op]
			self.t1[self.num] = [t1]
			self.t2[self.num] = [t2]
			self.v1[self.num] = [v1]
			self.v2[self.num] = [v2]
			self.busy[self.num] = [busy]
		else:
			self.op[index].append(op)
			self.t1[index].append(t1)
			self.t2[index].append(t2)
			self.v1[index].append(v1)
			self.v2[index].append(v2)
			self.busy[index].append(busy)
			
		self.num = self.num + 1

		return self.rsIndex + index


	def getSize():
		return self.size

	def getNum():
		return self.num

def printRFRAT(rf, rat):
	print("\tRF\t\tRAT")
	for i in range(0, len(rf.rf)):
		ratStr = ""
		if(rat.rf[i] != None):
			ratStr = "RS" + str(rat.rf[i])
		print("%d:\t%d\t\t%s" % (i, rf.rf[i], ratStr))

def cleanArrStr(arrStr):
	arrStr = arrStr.replace("None", "N")
	arrStr = arrStr.replace("[", "")
	arrStr = arrStr.replace("]", "")
	return arrStr
		
def printReserves(addRes, multRes):
	print("{:<14} {:<14} {:<14} {:<14} {:<14} {:<14} {:<14} {:<14}".format("", "Busy", "OP", "Vj", "Vk", "Qj", "Qk", "Disp/Cycle"))
	
	# Print addRes
	for i in range(0, addRes.size):
		if(addRes.op[0] != None):
			busy = [1]*len(addRes.busy[i])
		else:
			busy = [0]
		print("{:<14} {:<14} {:<14} {:<14} {:<14} {:<14} {:<14} {:<14}".format("RS" + str(addRes.rsIndex + i), cleanArrStr(str(busy)),  cleanArrStr(str(addRes.op[i])),  cleanArrStr(str(addRes.v1[i])),  cleanArrStr(str(addRes.v2[i])),  cleanArrStr(str(addRes.t1[i])),  cleanArrStr(str(addRes.t2[i])),  cleanArrStr(str(addRes.busy[i]))))

	# Print multRes
	for i in range(0, multRes.size):
		if(multRes.op[0] != None):
			busy = [1]*len(multRes.busy[i])
		else:
			busy = [0]
		print("{:<14} {:<14} {:<14} {:<14} {:<14} {:<14} {:<14} {:<14}".format("RS" + str(multRes.rsIndex + i), cleanArrStr(str(busy)),  cleanArrStr(str(multRes.op[i])),  cleanArrStr(str(multRes.v1[i])),  cleanArrStr(str(multRes.v2[i])),  cleanArrStr(str(multRes.t1[i])),  cleanArrStr(str(multRes.t2[i])),  cleanArrStr(str(multRes.busy[i]))))	
	
def instrParse(instr):
	return Instr(instr[0], instr[1], instr[2], instr[3])

def sim(file):
	# Read input file
	file = open(file, 'r')
	data = file.readlines()
	file.close()

	# Set number of instructions & number of cycles
	numInstr = int(data[0])
	numCycles = int(data[1])

	# Read instr
	instrs = data[2 : int(numInstr) + 2]
	instrs = [instrParse(x[:-1].split()) for x in instrs] # clean data (remove \n)

	# Create Instruction Queue
	iq = InstrQueue(instrs)

	# Read init RF values
	rf = data[int(numInstr) + 2 : len(data)]
	rf = RF([int(x[:-1]) for x in rf]) # clean data (remove \n) & convert str to int

	# Init RAT
	rat = RAT()

	# Init reserves
	addRes = Reserve(3, 1) # RS1 - RS3
	multRes = Reserve(2, 4) # RS4 - RS5

	# Init vars
	cycle = 0 # cpu cycle

	# Sim loop
	instrs = []
	for i in range(0, numCycles):
		instrs.append(iq.execNextInstr(rf, rat, addRes, multRes, cycle))
		rsWaitBroad = []
		firstElement = True
		for instr in instrs:
			depWait1 = rsWaitBroad.count(instr.src1) > 0
			depWait2 = rsWaitBroad.count(instr.src2) > 0
			
			rsWaitBroad.append(instr.rst)
						
			instr.run(rf, rat, addRes, multRes, cycle, (depWait1 or depWait2), broadcastWait = not firstElement)
			if(instr.broadcasted == True and firstElement):
				instrs.pop(0)
			
			firstElement = False
		cycle = cycle + 1

	printReserves(addRes,multRes)
	print()
	printRFRAT(rf, rat)
	print()
	print(iq)

if __name__ == "__main__":
	if(len(sys.argv) > 1):
		print("Running simulation w/ input file: %s\n" % (sys.argv[1]))
		sim(sys.argv[1])
	else:
		print("Error: no input file given")
		exit()
