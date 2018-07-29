#  File: SparseMatrixCompression.py

#  Description: This program tests methods in the matrix class for sparse matrices

#  Developer: David Liddle

#  Date Created: 4/3/2018

#  Date Last Modified: 4/7/2018

class Link (object):
  def __init__ (self, col = 0, data = 0, next = None):
    self.col = col
    self.data = data
    self.next = next

  # return a String representation of a Link (col, data)
  def __str__ (self):
    s = ''
    s=str(self.data)
    return s

class LinkedList (object):
  def __init__ (self):
    self.first = None

  def insert_last (self, col, data):
    new_link = Link (col, data)
    current = self.first

    if (current == None):
      self.first = new_link
      return

    while (current.next != None):
      current = current.next

    current.next = new_link

  # return a String representation of a LinkedList
  def __str__ (self):
    current=self.first
    previous=self.first
    s=""
    if current==None:
      return s
    i=0
    while(current != None):
      if current.col>i:
        s+="0  "
      else:
        s+=str(current.data)+"  "
        previous=current
        current=current.next
      i+=1
    return s

class Matrix (object):
  def __init__ (self, row = 0, col = 0):
    self.row = row
    self.col = col
    self.matrix = []

  # perform assignment operation: matrix[row][col] = data
  def set_element (self, row, col, data):
    if self.col < col:
      return None
    elt=Link(col,data)
    list=self.matrix[row]
    current=list.first
    previous=list.first
    if current.col==col:
      list.first=elt
      elt.next=current.next
    while(current != None):
      previous=current
      current=current.next
      if current.col >= col:
         break
    if current==None:
      previous.next=elt
    elif current.col==col:
      previous.next=elt
      elt.next=current.next
    else:
      previous.next=elt
      elt.next=current
  
    return

  # add two sparse matrices
  def __add__ (self, other):
    if ((self.row != other.row) or (self.col != other.col)):
      return None

    mat = Matrix (self.row, self.col)
    for i in range (self.row):
      eltA=self.matrix[i].first
      eltB=other.matrix[i].first
      new_row = LinkedList()
      for j in range (self.col):
        if eltA == None or eltA.col != j:
           if eltB.col == j:
             new_row.insert_last(j, eltB)
             eltB=eltB.next
        elif eltB == None or eltB.col != j:
          if eltA.col == j:
            new_row.insert_last(j, eltA)
            eltA=eltA.next
        else:
          elt = int (eltA.data+eltB.data)
          if (elt != 0):
            new_row.insert_last(j, elt)
          eltA=eltA.next
          eltB=eltB.next
      mat.matrix.append (new_row)
    return mat

  # multiply two sparse matrices
  def __mul__ (self, other):
    if self.col != other.row:
      return None
    mat=Matrix(self.row,  other.col)
    for h in range(self.row):
      new_row=LinkedList()
      for i in range(other.col):
        sum_mult=0
        currentA=self.matrix[h].first
        for j in range(other.row):
          eltA=currentA.data
          currentB=other.matrix[j].first
          eltB=currentB.data
          for k in range(i):
            currentB=currentB.next
            if currentB==None:
              eltB=0
              break
            elif currentB.col>i:
              eltB=0
              break
            eltB=currentB.data
          if currentA.col>j:
            eltA=0
            sum_mult+=0
          else:
           sum_mult+=eltA*eltB
           currentA=currentA.next
        if sum_mult != 0:
          new_row.insert_last(i,sum_mult)
      mat.matrix.append(new_row)    
    return mat

  # return a list representing a row with the zero elements inserted
  def get_row (self, n):
    row=self.matrix[n]
    elt=row.first
    s=list()
    for i in range(self.col):
      if elt.col>i:
        s.append(0)
      else:
        s.append(elt.data)
        elt=elt.next
    return s

  # return a list representing a column with the zero elements inserted
  def get_col (self, n):
    s=list()
    for i in range(self.row):
      row=self.matrix[i]
      elt=row.first
      for j in range(self.col):
        if elt == None:
          s.append(0)
          break
        elif elt.col == n:
          s.append(elt.data)
          break
        elif elt.col > n:
          s.append(0)
          break
        elt=elt.next
    return s

  # return a String representation of a matrix
  def __str__ (self):
    s = ''
    for row in self.matrix:
      line=str(row)
      line=line.split()
      c=0
      for i in range(len(line)):
        c+=1
        s+='{:>5}'.format(line[i])
      while(self.col > c):
       s+='{:>5}'.format("0")
       c+=1
      s+="\n"
    return s

def read_matrix (in_file):
  line = in_file.readline().rstrip("\n").split()
  row = int (line[0])
  col = int (line[1])
  mat = Matrix (row, col)

  for i in range (row):
    line = in_file.readline().rstrip("\n").split()
    new_row = LinkedList()
    for j in range (col):
      elt = int (line[j])
      if (elt != 0):
        new_row.insert_last(j, elt)
    mat.matrix.append (new_row)
  line = in_file.readline()

  return mat

def main():
  in_file = open ("./matrix.txt", "r")

  print ("Test Matrix Addition")
  matA = read_matrix (in_file)
  print (matA)
  matB = read_matrix (in_file)
  print (matB)

  matC = matA + matB
  print (matC)

  print ("\nTest Matrix Multiplication")
  matP = read_matrix (in_file)
  print (matP)
  matQ = read_matrix (in_file)
  print (matQ)
  matR = matP * matQ
  print (matR)

  print ("\nTest Setting a Zero Element to a Non-Zero Value")
  matA.set_element (1, 1, 5)
  print (matA)

  print ("\nTest Setting a Non-Zero Elements to a Zero Value")
  matB.set_element (1, 1, 0)
  print (matB)

  print ("\nTest Getting a Row")
  row = matP.get_row(1)
  print (row)

  print ("\nTest Getting a Column")
  col = matQ.get_col(0)
  print (col)
  
  in_file.close()

main()
