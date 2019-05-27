# DistanceVectorRouting
An interactive simulator for the distance-vector routing protocol in Python.

Run the program with the following command:
```
python main.py [coordinate file] [link file]
```

There are several different graphs files included, such as **coord_inf.txt** and 
its corresponding **links_inf.txt**, which will demonstrate the count-to-infinity
problem if link C-E fails.

You can create your own graph by making a coordinate file with the following syntax:
```
<name>, <x-coordinate>, <y-coordinate>
```
and its corresponding link file must be written in this form:
```
<start node name>, <end node name>, <weight>
```

The program is round-based with all propogation, transmission, and queueing 
delays assumed to be zero. At the start, nodes are only aware of distances to 
their immediate neighbors. Go to the next round by pressing the 'advance' button 
and the new routing tables will be displayed. 

Clicking on a node will display all the paths other nodes use to get there.
Clicking on a link will cause the link to fail (all failed links highlighted in
red) and clicking on it a second time will bring the link back up.

