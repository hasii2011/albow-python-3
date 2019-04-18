#-----------------------------------------------------------------------------
#
#   Albow - Profiling
#
#-----------------------------------------------------------------------------

from time import time

enable = False
stack = []
t_last_begin_frame = 0.0
t_used = 0.0
indent = "    "
label_width = 0

def start_profiling(frame_time):
	global target_frame_time, enable
	target_frame_time = frame_time
	enable = True
	del stack[:]

def stop_profiling():
	global enable
	enable = False

def begin(label):
	if enable:
		global label_width
		label_width = max(label_width, len(label))
		stack.append([label, time()])

def end(label):
	if enable:
		global t_used
		t1 = time()
		s = stack
		while s:
			item = s.pop()
			item_label = item[0]
			t0 = item[1]
			t = t1 - t0
			print("%s%8.6f %s" % (indent * (len(s) + 1), t, item_label))
			if not s:
				t_used += t
			if item_label == label:
				break

def begin_frame():
	if enable:
		global t_last_begin_frame, t_used
		t0 = t_last_begin_frame
		t1 = time()
		tf = t1 - t0
		tu = t_used
		ts = target_frame_time - tu
		pf = 100.0 * tf / target_frame_time
		ps = 100.0 * ts / target_frame_time
		print("%8.6f Frame (%3.0f%%) Used: %8.6f Spare: %8.6f (%3.0f%%)" % (
			tf, pf, tu, ts, ps))
		t_last_begin_frame = t1
		t_used = 0.0
