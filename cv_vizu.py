#!/usr/bin/python3

from event_log_parser import parse_events, batch_events
from layout_parser import collect_layout_nodes

from glob import glob
import cv2

cap = cv2.VideoCapture('telemetry/const.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print("Video runs at {} fps for {} frames".format(fps, frames))

fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (1200, 2000))

events = parse_events('telemetry/event-log.txt')
batched = batch_events(fps, int(frames), events)
current_frame = 42

xml_layouts = glob('telemetry/*.xml')
layouts = []
for xml in xml_layouts:
    layouts.append(collect_layout_nodes(xml))

cur_layout = 0

while(cap.isOpened):
    ret, frame = cap.read()
    fixed = cv2.resize(frame, (1200, 2000), cv2.INTER_AREA)

    try:
        for node in layouts[cur_layout]:
            fixed = cv2.rectangle(fixed, tuple(node.top_left), tuple(node.bottom_right), (0, 255, 0), thickness=3)
    except:
        pass
    
    try:
        for event in batched[current_frame]:
            fixed = cv2.circle(fixed, (event.x, event.y), 30, (0, 0, 255), -1)
    except:
        pass

    cv2.imshow("Recorded activity", fixed)
    out.write(fixed)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # cv2.waitKey()

    current_frame += 1
    cur_layout = int(current_frame // fps)

cap.release()
out.release()
cv2.destroyAllWindows()
