from binarytree import Node
from Tkinter import *
import tkFileDialog
import time

window_width = 850
sls = None
intersection_discovered = False
intersection_point = None
p = []
point_set = []
prev = None
browse_clicked = False
point_index = 0
test = None
automate_clicked = False


# Class to represent an end-point. It has x,y coordinates, a next and prev variables to store the next and previous
# points and an index to know the index of the point.
class Point:
    def __init__(self, x, y, i):
        self.x = x
        self.y = y
        self.index = i
        self.next_point = None
        self.prev_point = None

    def set_next(self, point):
        self.next_point = point

    def set_prev(self, point):
        self.prev_point = point


# Class to represent a line segment. It has start and end points of type Point, a label to store the name of the
# line segment and an index to know the index of the line segment.
class LineSegment:
    def __init__(self, start, end, i):
        self.start = start
        self.end = end
        self.label = "S" + str(i)
        self.index = i


# This fucntion finds predecessor and successor of key in BST
# It sets pre and suc as predecessor and successor respectively
def findPreSuc(root, key):
    # Base Case
    if root is None or root.data is None:
        return

    # If key is present at root
    if root.data.start.x == key.start.x and root.data.start.y == key.start.y and \
            root.data.end.x == key.end.x and root.data.end.y == key.end.y:

        # the maximum value in left subtree is predecessor
        if root.left is not None:
            tmp = root.left
            while tmp.right:
                tmp = tmp.right
            findPreSuc.pre = tmp

        # the minimum value in right subtree is successor
        if root.right is not None:
            tmp = root.right
            while tmp.left:
                tmp = tmp.left
            findPreSuc.suc = tmp

        return

    # If x-coordinate of start point of root is greater than x-coordinate of start point of key, go to left subtree
    # If x-coordinate of start point of root is lesser than x-coordinate of start point of key, go to right subtree
    # If they are equal, we do the above for the y-coordinate of start points for key and root.
    # If they are equal, we do the above for the x-coordinate of end points for key and root.
    # If they are equal, we do the above for the y-coordinate of end points for key and root.
    if root.data.start.x > key.start.x:
        findPreSuc.suc = root
        findPreSuc(root.left, key)
    elif root.data.start.x < key.start.x:
        findPreSuc.pre = root
        findPreSuc(root.right, key)
    else:
        if root.data.start.y > key.start.y:
            findPreSuc.suc = root
            findPreSuc(root.left, key)
        elif root.data.start.y < key.start.y:
            findPreSuc.pre = root
            findPreSuc(root.right, key)
        else:
            if root.data.end.x > key.end.x:
                findPreSuc.suc = root
                findPreSuc(root.left, key)
            elif root.data.end.x < key.end.x:
                findPreSuc.pre = root
                findPreSuc(root.right, key)
            else:
                if root.data.end.y > key.end.y:
                    findPreSuc.suc = root
                    findPreSuc(root.left, key)
                elif root.data.end.y < key.end.y:
                    findPreSuc.pre = root
                    findPreSuc(root.right, key)
                else:
                    findPreSuc.pre = root
                    findPreSuc(root.right, key)

# Verify if a point r lies on a segment pq
def on_segment(p, q, r):
    if max(p.x, r.x) >= q.x >= min(p.x, r.x) and max(p.y, r.y) >= q.y >= min(p.y, r.y):
        return True

    return False

# Left test of r on pq
def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    if val > 0:
        return 1
    if val < 0:
        return 2

# Check if p1q1 and p2q2 intersects
def do_intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, p2, q1):
        return True

    if o2 == 0 and on_segment(p1, q2, q1):
        return True

    if o3 == 0 and on_segment(p2, p1, q2):
        return True

    if o4 == 0 and on_segment(p2, q1, q2):
        return True

# Get the intersection point of segment1 and segment2
def get_intersection_point(segment1, segment2):
    a1 = segment1.end.y - segment1.start.y
    b1 = segment1.start.x - segment1.end.x
    c1 = a1 * segment1.start.x + b1 * segment1.start.y

    a2 =segment2.end.y - segment2.start.y
    b2 = segment2.start.x - segment2.end.x
    c2 = a2 * segment2.start.x + b2 * segment2.start.y

    determinant = a1 * b2 - a2 * b1
    if determinant != 0:
        x = float((b2 * c1 - b1 * c2)) / determinant
        y = float((a1 * c2 - a2 * c1)) / determinant
        cross_point = Point(round(x,2), round(y,2), -1)
        return cross_point


def pre_process_points(points):
    global stop_y
    global sls
    global intersection_discovered
    global intersection_point

    for i in xrange(len(points)):
        print "Coordinates = " + str(points[i].x) + "," + str(points[i].y)

    # Sort the points in the event queue by y-coordinate
    event_queue = sorted(points, key=lambda point: point.y)
    last_point = 0
    sls = None
    index = 0
    # Consider each point in the event queue
    for current_point in event_queue:
        stop_y = current_point.y - last_point
        # If the current point has a previous point, insert that line segment into the sls
        if current_point.prev_point is not None:
            line_segment_1 = LineSegment(current_point, current_point.prev_point, current_point.prev_point.index)
            line_segment_1_dup = LineSegment(current_point.prev_point, current_point,
                                             current_point.prev_point.index)
            if sls is None:
                sls = Node(line_segment_1)
                index = index + 1
            else:
                # Verify that line segment is not already present
                lsegment = sls.lookup(line_segment_1)
                rsegment = sls.lookup(line_segment_1_dup)
                if lsegment[0] is None and rsegment[0] is None:
                    sls.insert(line_segment_1)
                    index = index + 1
                    findPreSuc.pre = None
                    findPreSuc.suc = None
                    findPreSuc(sls, line_segment_1)

                    # Check for intersection with predecessor
                    if findPreSuc.pre is not None and abs(findPreSuc.pre.data.index - line_segment_1.index) > 1:
                        if do_intersect(findPreSuc.pre.data.start, findPreSuc.pre.data.end,
                                        line_segment_1.start,
                                        line_segment_1.end):
                            print "Predecessor is", findPreSuc.pre.data.label, "{(", \
                                findPreSuc.pre.data.start.x, ",", findPreSuc.pre.data.start.y, "),(", \
                                findPreSuc.pre.data.end.x, ",", findPreSuc.pre.data.end.y, ")}"
                            print "Current Point is", line_segment_1.label, "{(", \
                                line_segment_1.start.x, ",", line_segment_1.start.y, "),(", \
                                line_segment_1.end.x, ",", line_segment_1.end.y, ")}"
                            print "Intersection Discovered1"
                            intersection_discovered = True
                            intersection_point = get_intersection_point(findPreSuc.pre.data, line_segment_1)
                            if automate_clicked:
                                if test is not None:
                                    sls_canvas.delete(test)
                                test = sls_canvas.create_text(window_width/2, 20, fill="darkblue", font="Times 20 italic bold",
                                                              text="Intersection Discovered at ("+str(intersection_point.x)+
                                                                   ", "+str(intersection_point.y)+")", anchor = CENTER)
                                child_canvas.create_oval(intersection_point.x - 2.0, intersection_point.y - 2.0,
                                                         intersection_point.x + 2.0,
                                                         intersection_point.y + 2.0,
                                                         outline="red", fill="red", width=2)

                    # Check for intersection with successor
                    if findPreSuc.suc is not None and abs(findPreSuc.suc.data.index - line_segment_1.index) > 1:
                        if do_intersect(findPreSuc.suc.data.start, findPreSuc.suc.data.end,
                                        line_segment_1.start,
                                        line_segment_1.end):
                            print "Successor is", findPreSuc.suc.data.label, "{(", \
                                findPreSuc.suc.data.start.x, ",", findPreSuc.suc.data.start.y, "),(", \
                                findPreSuc.suc.data.end.x, ",", findPreSuc.suc.data.end.y, ")}"
                            print "Current Point is", line_segment_1.label, "{(", \
                                line_segment_1.start.x, ",", line_segment_1.start.y, "),(", \
                                line_segment_1.end.x, ",", line_segment_1.end.y, ")}"
                            print "Intersection Discovered2"
                            intersection_discovered = True
                            intersection_point = get_intersection_point(findPreSuc.suc.data, line_segment_1)
                            if automate_clicked:
                                if test is not None:
                                    sls_canvas.delete(test)
                                test = sls_canvas.create_text(window_width/2, 20, fill="darkblue", font="Times 20 italic bold",
                                                              text="Intersection Discovered at (" + str(intersection_point.x) +
                                                                   ", " + str(intersection_point.y) + ")", anchor = CENTER)
                                child_canvas.create_oval(intersection_point.x - 2.0, intersection_point.y - 2.0,
                                                         intersection_point.x + 2.0,
                                                         intersection_point.y + 2.0,
                                                         outline="red", fill="red", width=2)
                else:
                    # If the line segment already exists in the sls, delete it
                    if lsegment[0] is not None:
                        findPreSuc.pre = None
                        findPreSuc.suc = None
                        findPreSuc(sls, lsegment[0].data)
                        sls.delete(lsegment[0].data)
                    else:
                        findPreSuc.pre = None
                        findPreSuc.suc = None
                        findPreSuc(sls, rsegment[0].data)
                        sls.delete(rsegment[0].data)

                    # Check for intersection with new successor and predecessor
                    if findPreSuc.pre is not None and findPreSuc.suc is not None and \
                            abs(findPreSuc.pre.data.index - findPreSuc.suc.data.index) > 1 and\
                            do_intersect(findPreSuc.pre.data.start, findPreSuc.pre.data.end,
                                    findPreSuc.suc.data.start,
                                    findPreSuc.suc.data.end):
                        print "Predecessor is", findPreSuc.pre.data.label, "{(", \
                            findPreSuc.pre.data.start.x, ",", findPreSuc.pre.data.start.y, "),(", \
                            findPreSuc.pre.data.end.x, ",", findPreSuc.pre.data.end.y, ")}"
                        print "Successor is", findPreSuc.suc.data.label, "{(", \
                            findPreSuc.suc.data.start.x, ",", findPreSuc.suc.data.start.y, "),(", \
                            findPreSuc.suc.data.end.x, ",", findPreSuc.suc.data.end.y, ")}"
                        print "Intersection Discovered3"
                        intersection_discovered = True
                        intersection_point = get_intersection_point(findPreSuc.pre.data, findPreSuc.suc.data)
                        if automate_clicked:
                            if test is not None:
                                sls_canvas.delete(test)
                            test = sls_canvas.create_text(window_width/2, 20, fill="darkblue", font="Times 20 italic bold",
                                                          text="Intersection Discovered at (" + str(intersection_point.x) +
                                                               ", " + str(intersection_point.y) + ")", anchor = CENTER)
                            child_canvas.create_oval(intersection_point.x - 2.0, intersection_point.y - 2.0,
                                                     intersection_point.x + 2.0,
                                                     intersection_point.y + 2.0,
                                                     outline="red", fill="red", width=2)
                        return

        # If the current point has a next point, insert that line segment into the sls
        if current_point.next_point is not None:
            line_segment_2 = LineSegment(current_point, current_point.next_point, current_point.index)
            line_segment_2_dup = LineSegment(current_point.next_point, current_point,
                                             current_point.index)
            if sls is None:
                sls = Node(line_segment_2)
                index = index + 1
            else:
                lsegment = sls.lookup(line_segment_2)
                rsegment = sls.lookup(line_segment_2_dup)
                # Verify that line segment is not already present
                if lsegment[0] is None and rsegment[0] is None:
                    sls.insert(line_segment_2)
                    index = index + 1
                    findPreSuc.pre = None
                    findPreSuc.suc = None
                    findPreSuc(sls, line_segment_2)
                    # Check for intersection with predecessor
                    if findPreSuc.pre is not None and abs(findPreSuc.pre.data.index - line_segment_2.index) > 1:
                        if do_intersect(findPreSuc.pre.data.start, findPreSuc.pre.data.end,
                                        line_segment_2.start,
                                        line_segment_2.end):
                            print "Predecessor is", findPreSuc.pre.data.label, "{(", \
                                findPreSuc.pre.data.start.x, ",", findPreSuc.pre.data.start.y, "),(", \
                                findPreSuc.pre.data.end.x, ",", findPreSuc.pre.data.end.y, ")}"
                            print "Current Point is", line_segment_2.label, "{(", \
                                line_segment_2.start.x, ",", line_segment_2.start.y, "),(", \
                                line_segment_2.end.x, ",", line_segment_2.end.y, ")}"
                            print "Intersection Discovered4"
                            intersection_discovered = True
                            intersection_point = get_intersection_point(findPreSuc.pre.data, line_segment_2)
                            if automate_clicked:
                                if test is not None:
                                    sls_canvas.delete(test)
                                test = sls_canvas.create_text(window_width/2, 20, fill="darkblue", font="Times 20 italic bold",
                                                              text="Intersection Discovered at (" + str(intersection_point.x) +
                                                                   ", " + str(intersection_point.y) + ")", anchor = CENTER)
                                child_canvas.create_oval(intersection_point.x - 2.0, intersection_point.y - 2.0,
                                                         intersection_point.x + 2.0,
                                                         intersection_point.y + 2.0,
                                                         outline="red", fill="red", width=2)
                            return

                    # Check for intersection with successor
                    if findPreSuc.suc is not None and abs(findPreSuc.suc.data.index - line_segment_2.index) > 1:
                        if do_intersect(findPreSuc.suc.data.start, findPreSuc.suc.data.end,
                                        line_segment_2.start,
                                        line_segment_2.end):
                            print "Successor is", findPreSuc.suc.data.label, "{(", \
                                findPreSuc.suc.data.start.x, ",", findPreSuc.suc.data.start.y, "),(", \
                                findPreSuc.suc.data.end.x, ",", findPreSuc.suc.data.end.y, ")}"
                            print "Current Point is", line_segment_2.label, "{(", \
                                line_segment_2.start.x, ",", line_segment_2.start.y, "),(", \
                                line_segment_2.end.x, ",", line_segment_2.end.y, ")}"
                            print "Intersection Discovered5"
                            intersection_discovered = True
                            intersection_point = get_intersection_point(findPreSuc.suc.data, line_segment_2)
                            if automate_clicked:
                                if test is not None:
                                    sls_canvas.delete(test)
                                test = sls_canvas.create_text(window_width/2, 20, fill="darkblue", font="Times 20 italic bold",
                                                              text="Intersection Discovered at (" + str(intersection_point.x) +
                                                                   ", " + str(intersection_point.y) + ")", anchor = CENTER)
                                child_canvas.create_oval(intersection_point.x - 2.0, intersection_point.y - 2.0,
                                                         intersection_point.x + 2.0,
                                                         intersection_point.y + 2.0,
                                                         outline="red", fill="red", width=2)
                            return
                else:
                    # If the line segment already exists in the sls, delete it
                    if lsegment[0] is not None:
                        findPreSuc.pre = None
                        findPreSuc.suc = None
                        findPreSuc(sls, lsegment[0].data)
                        sls.delete(lsegment[0].data)
                    else:
                        findPreSuc.pre = None
                        findPreSuc.suc = None
                        findPreSuc(sls, rsegment[0].data)
                        sls.delete(rsegment[0].data)

                    # Check for intersection with new successor and predecessor
                    if findPreSuc.pre is not None and findPreSuc.suc is not None and \
                            abs(findPreSuc.pre.data.index - findPreSuc.suc.data.index) > 1 and \
                            do_intersect(findPreSuc.pre.data.start, findPreSuc.pre.data.end,
                                    findPreSuc.suc.data.start,
                                    findPreSuc.suc.data.end):
                        print "Predecessor is", findPreSuc.pre.data.label, "{(", \
                            findPreSuc.pre.data.start.x, ",", findPreSuc.pre.data.start.y, "),(", \
                            findPreSuc.pre.data.end.x, ",", findPreSuc.pre.data.end.y, ")}"
                        print "Successor is", findPreSuc.suc.data.label, "{(", \
                            findPreSuc.suc.data.start.x, ",", findPreSuc.suc.data.start.y, "),(", \
                            findPreSuc.suc.data.end.x, ",", findPreSuc.suc.data.end.y, ")}"
                        print "Intersection Discovered6"
                        intersection_discovered = True
                        intersection_point = get_intersection_point(findPreSuc.pre.data, findPreSuc.suc.data)
                        if automate_clicked:
                            if test is not None:
                                sls_canvas.delete(test)
                            test = sls_canvas.create_text(window_width/2, 20, fill="darkblue", font="Times 20 italic bold",
                                                          text="Intersection Discovered at (" + str(intersection_point.x) +
                                                               ", " + str(intersection_point.y) + ")", anchor = CENTER)
                            child_canvas.create_oval(intersection_point.x - 2.0, intersection_point.y - 2.0, intersection_point.x + 2.0,
                                                     intersection_point.y + 2.0,
                                                     outline="red", fill="red", width=2)
                        return

        if not automate_clicked:
            button4.wait_variable(var)
            var.set(0)
        if intersection_discovered:
            return

        label = ""
        global test
        if sls.data is not None:
            sls_text = sls.print_tree(label)
            if test is not None:
                sls_canvas.delete(test)
            test = sls_canvas.create_text(window_width/2, 20, fill="darkblue", font="Times 20 italic bold", anchor = CENTER,
                                          text=sls_text)
            print label

        last_point = current_point.y

    print "This is a simple chain"
    global button4
    if test is not None:
        sls_canvas.delete(test)
    test = sls_canvas.create_text(window_width/2, 20, fill="green", font="Times 20 italic bold", anchor = CENTER,
                                  text="This is a simple chain")

    button4.config(state="disabled")


def callback(event):
    global p
    global point_set
    global prev
    global point_index
    global browse_clicked
    w.focus_set()
    print event.x, event.y
    button5.config(state="disabled")
    button6.config(state="normal")
    if not browse_clicked:
        current_point = Point(event.x, event.y, point_index)
        point_index = point_index + 1
        current_point.set_prev(prev)
        if prev is not None:
            prev.set_next(current_point)
        child_canvas.create_oval(current_point.x - 2, current_point.y - 2, current_point.x + 2, current_point.y + 2,
                                 outline="purple", fill="purple", width=2)
        point_set.append(current_point)
        p.append(current_point)
        prev = current_point
        if len(p) == 2:
            child_canvas.create_line(p[0].x, p[0].y, p[1].x, p[1].y, width=2)
            p.pop(0)


# Callback function to start the sweep algorithm
def button_callback():
    global point_set
    global button1
    button1.config(state="disabled")
    start = time.time()
    pre_process_points(point_set)
    end = time.time()
    print(end - start)


# Callback function to exit the application
def exit_callback():
    master.destroy()


# Callback function to reset all the changes
def reset_callback():
    global point_set
    global p
    global browse_clicked
    global sls
    global intersection_discovered
    global prev
    global point_index
    global test
    global sweep_line
    global sweep_status
    #global automate_clicked

    automate_clicked = False
    browse_clicked = False
    button5.config(state="normal")
    button6.config(state="disabled")
    button1.config(state="normal")
    button7.config(state="normal")
    point_set = []
    p = []
    sls = None
    intersection_discovered = False
    prev = None
    point_index = 0
    test = None
    child_canvas.delete("all")
    sls_canvas.delete("all")
    sweep_line = child_canvas.create_line(0, 0, window_width, 0, fill="red")
    sweep_status = True
    automate_clicked = True
    intersection_point = None


# Callback function to go to the next step in the algorithm
def next_callback():
    global intersection_discovered
    animation()
    var.set(1)
    if intersection_discovered:
        global test
        if test is not None:
            sls_canvas.delete(test)
        test = sls_canvas.create_text(window_width/2, 20, fill="darkblue", font="Times 20 italic bold",
                                      text="Intersection Discovered at (" + str(intersection_point.x) +
                                                               ", " + str(intersection_point.y) + ")", anchor = CENTER)
        child_canvas.create_oval(intersection_point.x - 2.0, intersection_point.y - 2.0, intersection_point.x + 2.0,
                                 intersection_point.y + 2.0,
                                 outline="red", fill="red", width=2)


# Callback function to browse for a text file to load into the program
def browse_callback():
    global p
    global point_set
    global prev
    global point_index
    global browse_clicked

    master.filename = tkFileDialog.askopenfilename(initialdir=".", title="Select file",
                                                   filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    reset_callback()
    print (master.filename)
    text_input = open(master.filename)
    browse_clicked = True
    inputs = text_input.readlines()
    for current_input in inputs:
        coordinates = current_input.split()
        current_point = Point(int(coordinates[0]), int(coordinates[1]), point_index)
        point_index = point_index + 1
        current_point.set_prev(prev)

        if prev is not None:
            prev.set_next(current_point)
        child_canvas.create_oval(current_point.x - 2, current_point.y - 2, current_point.x + 2, current_point.y + 2,
                                 outline="purple", fill="purple", width=2)
        point_set.append(current_point)
        p.append(current_point)
        prev = current_point
        if len(p) == 2:
            child_canvas.create_line(p[0].x, p[0].y, p[1].x, p[1].y, width=2)
            p.pop(0)


# Callback function to save the current set of points
def save_callback():
    f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    for single_point in point_set:
        f.write(str(single_point.x) + " " + str(single_point.y) + "\n")
    f.close()


# Function to animate the sweep line status
def animation():
    exit_val = 0
    while True:
        x = 0
        y = 1
        if exit_val == 0:
            for i in range(0, stop_y):
                time.sleep(0.025)
                child_canvas.move(sweep_line, x, y)
                child_canvas.update()
            exit_val = 1
        else:
            break


# Callback function to disable animation
def automate_callback():
    global automate_clicked
    automate_clicked = True
    button7.config(state="disabled")


stop_y = 0
master = Tk()
master.title("Bentley Ottmann Sweep")

var = IntVar()
w = Canvas(master, width=window_width, height=500)
inframe = Frame()
child_canvas = Canvas(inframe, width=window_width - 5, height=415, bd=2, relief="ridge")
child_canvas.pack()
child_canvas.bind("<Button-1>", callback)
child_canvas.addtag_all("test")

sls_frame = Frame()
sls_canvas = Canvas(sls_frame, width=window_width - 5, height=30, bd=2, relief="ridge")
sls_canvas.pack()
sls_canvas.addtag_all("sls")
sls_canvas_window = w.create_window(0, 40, anchor=NW, window=sls_frame)

test_canvas = w.create_window(0, 80, anchor=NW, window=inframe)
w.pack()
button1 = Button(master, text="Start Sweep", command=button_callback, anchor=W)
button1.configure(width=10, activebackground="#33B5E5", relief=FLAT)
button1_window = w.create_window(10, 10, anchor=NW, window=button1)

button2 = Button(master, text="Exit", command=exit_callback, anchor=W)
button2.configure(width=10, activebackground="#33B5E5", relief=FLAT)
button2_window = w.create_window(730, 10, anchor=NW, window=button2)

button3 = Button(master, text="Reset", command=reset_callback, anchor=W)
button3.configure(width=10, activebackground="#33B5E5", relief=FLAT)
button3_window = w.create_window(250, 10, anchor=NW, window=button3)

button4 = Button(master, text="Next", command=next_callback, anchor=W)
button4.configure(width=10, activebackground="#33B5E5", relief=FLAT)
button4_window = w.create_window(130, 10, anchor=NW, window=button4)

button5 = Button(master, text="Browse", command=browse_callback, anchor=W)
button5.configure(width=10, activebackground="#33B5E5", relief=FLAT)
button5_window = w.create_window(490, 10, anchor=NW, window=button5)

button6 = Button(master, text="Save", command=save_callback, anchor=W)
button6.configure(width=10, activebackground="#33B5E5", relief=FLAT)
button6_window = w.create_window(370, 10, anchor=NW, window=button6)
button6.config(state="disabled")

button7 = Button(master, text="Automate", command=automate_callback, anchor=W)
button7.configure(width=10, activebackground="#33B5E5", relief=FLAT)
button7_window = w.create_window(610, 10, anchor=NW, window=button7)

sweep_line = child_canvas.create_line(0, 0, window_width, 0, fill="red", activewidth=2)
sweep_status = True

mainloop()
