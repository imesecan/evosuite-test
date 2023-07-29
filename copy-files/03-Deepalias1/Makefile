.DEFAULT_GOAL := clean

clean: folders files
	find src/ -name *.class | xargs rm -f {} 

folders:
	rm -rf  __pycache__  target/  src/main/java/__pycache__  src/test

files:
	rm -rf  best/*.java  
