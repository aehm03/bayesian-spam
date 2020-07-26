get_data:
	curl -o data/raw/enron1.tar.gz  http://nlp.cs.aueb.gr/software_and_datasets/Enron-Spam/preprocessed/enron1.tar.gz
	tar -xf data/raw/enron1.tar.gz -C data/raw/ -m