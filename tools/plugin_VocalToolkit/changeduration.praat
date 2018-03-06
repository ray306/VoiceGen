form Change duration
	positive New_duration_(s) 3.0
	choice Method 1
		button Stretch
		button Cut/add time
endform
include batch.praat
procedure action
	s$ = selected$("Sound")
	wrk = Copy... wrk
	execute fixdc.praat
	dur = Get total duration
	if 'dur:2' <> 'new_duration:2'
		if method = 1
			factor = 'new_duration'/'dur'
			if factor > 3
				factor = 3
			endif
include minmaxf0.praat
			result = Lengthen (overlap-add)... 'minF0' 'maxF0' 'factor'
			result_duration = Get total duration
			if 'result_duration:2' <> 'new_duration:2'
				repeat
					result_tmp = selected("Sound")
					factor = 'new_duration'/'result_duration'
					if factor > 3
						factor = 3
					endif
					result = Lengthen (overlap-add)... 'minF0' 'maxF0' 'factor'
					result_duration = Get total duration
					select result_tmp
					Remove
					select result
				until 'result_duration:2' >= 'new_duration:2'
			endif
		elsif method = 2
			result = Extract part... 0 new_duration rectangular 1 no
		endif
	else
		result = Copy... result
	endif
	Rename... 's$'_changeduration_'method$'_'new_duration:2'
	execute fixdc.praat
	select wrk
	Remove
	select result
endproc
