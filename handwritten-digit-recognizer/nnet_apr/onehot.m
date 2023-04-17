
function Xloh=onehot(xl)
	labs=unique(xl);
	C=numel(labs);
	for c=1:C
		Xloh(c,:) = xl==labs(c);
	end
end
