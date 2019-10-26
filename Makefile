.PHONY: test
all: generatespec

generatespec:
	echo "Generating specifcation...."
	python3 ./script/generateSpecification.py -i ./organisasjoner.csv
clean:
	rm ./tmp/*.json
