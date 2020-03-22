.PHONY: all clean

Z3_INCLUDE ?= .
Z3_LIB ?= .

SRC_DIR = Source
INC_DIR = Header
OBJ_DIR = Object_Files

SRCS = $(SRC_Dir)/Dag.cpp $(SRC_Dir)/Formula.cpp $(SRC_Dir)/Formula_LTL.cpp $(SRC_Dir)/Formula_SLTL.cpp $(SRC_Dir)/Grammar.cpp $(SRC_Dir)/Main.cpp $(SRC_Dir)/Sample_Tracer.cpp $(SRC_Dir)/Sample_Tracer_LTL.cpp $(SRC_Dir)/Sample_Tracer_SLTL.cpp $(SRC_Dir)/Term_SLTL.cpp

CPPFLAGS += -g -Ofast -std=c++11

OBJ = $(OBJ_DIR)/Dag.o $(OBJ_DIR)/Formula.o $(OBJ_DIR)/Formula_LTL.o $(OBJ_DIR)/Formula_SLTL.o $(OBJ_DIR)/Grammar.o $(OBJ_DIR)/Sample_Tracer.o $(OBJ_DIR)/Sample_Tracer_LTL.o $(OBJ_DIR)/Sample_Tracer_SLTL.o $(OBJ_DIR)/Term_SLTL.o

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) -I . -I $(Z3_INCLUDE) $(CPPFLAGS) -c -o $@ $<

all: $(OBJ)
	$(CXX) -I . -I $(Z3_INCLUDE) -L $(Z3_LIB) -o flie $(SRC_DIR)/Main.cpp $(OBJ) -lz3

clean:
	rm -rf *.o
	rm -rf flie
	rm -rf flie.exe
