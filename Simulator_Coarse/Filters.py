def MeanFilter(input):
	(timeStamp, data) = input
	
	output = {}
	
	for componentName, signal in data.iteritems():
		mean = 0
		for dataPoint in signal:
			mean += dataPoint
		
		output[componentName] = mean/len(signal)
		
	return output