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
	def __str__(self):
		return str([self.op, self.rst, self.src1, self.src2])

	def __init__(self, op, rst, src1, src2):
		self.op = int(op)
		self.rst = int(rst)
		self.src1 = int(src1)
		self.src2 = int(src2)

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

	def issue(self):
		""

	def dispatch(self):
		""

	def broadcast(self):
		""

	def exec(self, rf, rat):
		# Execute instr
		match self.op:
			case 0:
				rf.setReg(self.rst, getReg(self.src1) + getReg(self.src2))
			case 1:
				rf.setReg(self.rst, getReg(self.src1) - getReg(self.src2))
			case 2:
				rf.setReg(self.rst, getReg(self.src1) * getReg(self.src2))
			case 3:
				rf.setReg(self.rst, getReg(self.src1) / getReg(self.src2))


class InstrQueue():
	# IQ
	def __init__(self, instrs):
		self.pc = 0	
		self.instrs = instrs

	def setPC(self, value):
		self.pc = value

	def getPC(self):
		return self.pc	

	def execNextInstr(self, rf):
		# reset pc counter if all instr are exec	
		if(self.pc == len(self.instrs)):
			self.pc = 0
		self.instrs[self.pc].exec(rf)
		self.pc = self.pc + 1

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
		self.num = 0	
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
		if(num = size):
			num = 0
	
		self.op[self.num] = op
		self.t1[self.num] = t1
		self.t2[self.num] = t2
		self.v1[self.num] = v1
		self.v2[self.num] = v2
		self.busy[self.num] = busy
		self.num = num + 1

		return self.rsIndex + self.num - 1


	def getSize():
		return self.size

	def getNum():
		return self.num 

def instrParse(instr):
	return Instr(instr[0], instr[1], instr[2], instr[3])

def sim(file):
	pc = 0
		

def readInputFile(file):
	file = open(file, 'r')
	data = file.readlines()
	file.close()
	numInstr = data[0]
	numCycles = data[1]
 	
	# Read instr
	instr = data[2 : int(numInstr) + 2]
	instr = [instrParse(x[:-1].split()) for x in instr] # clean data (remove \n)	
	print(instr)

	for i in instr:
		print(i.op)
		print(i.getCycles())

	iq = InstrQueue(instr)

	# Read init RF values
	rf = data[int(numInstr) + 2 : len(data)]
	rf = RF([int(x[:-1]) for x in rf]) # clean data (remove \n) & convert str to int
	print(rf)

	rat = RAT()	
	print(rat)

	addRes = Reserve(3, 1) # RS1 - RS3
	multRes = Reserve(2, 4) # RS4 - RS5

	
if __name__ == "__main__":
	if(len(sys.argv) > 1):
		print("Running simulation w/ input file: %s" % (sys.argv[1]))
		readInputFile(sys.argv[1])
	else:
		print("Error: no input file given")
		exit()	
