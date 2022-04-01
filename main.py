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

	def issue(self, depWait = False):
		if(not depWait):
			self.state = self.state + 1

	def dispatch(self):
		self.cycles = self.cycles + 1
		if(self.getCycles() == self.cycles):
			self.state = self.state + 1

	def broadcast(self, rf):
		pass
		#rf.setReg(self.rst, self.result)

	def run(self, rf, rat, addReserve, multReserve, cycle, depWait = False, broadcastWait = False):
		match self.state:
			case 0:
				self.issue(depWait)
			case 1:
				self.dispatch(broadcastWait)
			case 2:
				self.broadcast(rf)

		# Check for raw dep

		# Execute instr
		match self.op:
			case 0:
				""
				# ratRS = addReserve.addItem(0, None, None, None, None, cycle)
				# rat.setReg(self.rst, ratRS) # update RAT
				#rf.setReg(self.rst, getReg(self.src1) + getReg(self.src2))
			case 1:
				""
				# rf.setReg(self.rst, getReg(self.src1) - getReg(self.src2))
			case 2:
				""
				# rf.setReg(self.rst, getReg(self.src1) * getReg(self.src2))
			case 3:
				""
				# rf.setReg(self.rst, getReg(self.src1) / getReg(self.src2))


class InstrQueue():
	# IQ
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
		instr.run(rf, rat, addReserve, multReserve, cycle, depWait)
		self.pc = self.pc + 1

		return instr

class RF():
	def __str__(self):
		return str(self.rf)

	def __init__(self, rf = None, size = 8):
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
		super().__init__(range(0, size))

class Reserve():
	def __init__(self, size, rsIndex = 0):
		self.size = size
		self.num = 0 # number of items
		self.rsIndex = rsIndex

		self.op = [None]
		self.t1 = [None]
		self.t2 = [None]
		self.v1 = [None]
		self.v2 = [None]
		self.busy = [None]

	def set(self, op, t1, t2, v1, v2, busy, index):
		self.op[index] = op
		self.t1[index] = t1
		self.t2[index] = t2
		self.v1[index] = v1
		self.v2[index] = v2
		self.busy[index] = busy

	def addItem(self, op, t1, t2, v1, v2, busy):
		if(num == 0):
			self.op[index] = [op]
			self.t1[index] = [t1]
			self.t2[index] = [t2]
			self.v1[index] = [v1]
			self.v2[index] = [v2]
			self.busy[index] = [busy]

		index = num % size
		self.op[index].append(op)
		self.t1[index].append(t1)
		self.t2[index].append(t2)
		self.v1[index].append(v1)
		self.v2[index].append(v2)
		self.busy[index].append(busy)
		self.num = num + 1

		return self.rsIndex + self.index


	def getSize():
		return self.size

	def getNum():
		return self.num

def printRFRAT(rf, rat):
	print("\tRF\t\tRAT")
	for i in range(0, len(rf.rf)):
		print("%d:\t%d\t\tRS%d" % (i, rf.rf[i], rat.rf[i]))

def printReserves(addRes, multRes):
	print("\t\t\tBusy\t\t\tOP\t\t\tVj\t\t\tVk\t\t\tQj\t\t\tQk\t\t\tDisp")
	for i in range(0, addRes.size):
		if(addRes.op[0] != None):
			busy = [1]*len(addRes.busy)
		else:
			busy = [0]
		print("RS%d\t\t\t%s\t\t\t%s\t\t\t%s\t\t\t%s\t\t\t%s\t\t\t%s\t\t\t%s" % (addRes.rsIndex + i, busy, addRes.op, addRes.v1, addRes.v2, addRes.t1, addRes.t2, addRes.busy))

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
	instr = data[2 : int(numInstr) + 2]
	instr = [instrParse(x[:-1].split()) for x in instr] # clean data (remove \n)

	# Create Instruction Queue
	iq = InstrQueue(instr)

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
	#rawDep = []

	# Sim loop
	instr = []
	for i in range(0, numCycles):
		instr.append(iq.execNextInstr(rf, rat, addRes, multRes, cycle))
		rawDep = []
		for j in instr:
			if(j.state != 2):
				rawDep.append(j.rst)
			print(j.rst)
			print(rawDep)
			depWait1 = rawDep.count(j.src1) - 1 > 0
			depWait2 = rawDep.count(j.src2) - 1 > 0
			print("depWait:" + str(bool(depWait1)) + str(bool(depWait1)))
			j.run(rf, rat, addRes, multRes, cycle, depWait = (depWait1 or depWait2))
		#iq.issueNextInstr
		cycle = cycle + 1

	printReserves(addRes,multRes)
	printRFRAT(rf, rat)


if __name__ == "__main__":
	if(len(sys.argv) > 1):
		print("Running simulation w/ input file: %s" % (sys.argv[1]))
		sim(sys.argv[1])
	else:
		print("Error: no input file given")
		exit()
