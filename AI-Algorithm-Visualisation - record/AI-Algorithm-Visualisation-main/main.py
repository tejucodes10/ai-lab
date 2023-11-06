from SearchAgent import SearchAgent
from Node import Node
from SavedGraph import *
from browser import document, window, alert
import javascript, json

#changes_made = False
def update_graph():
    global any_change, colors_to_fill_inside, agent, radius, colors_for_border, node_type \
        ,animate, val, ctx, border, node_selected, selected_algorithm 
    #update_canvas_size()
    def draw_weights(node1, node2):
        global ctx
        ctx.font = "18px Arial"
        x1, y1 = agent.graph[node1].position
        x2, y2 = agent.graph[node2].position
        weight = agent.graph[node1].children[node2]
        ctx.fillText(weight,(x1+x2)/2, (y1+y2)/2)
    
    def draw_heuristics(node):
        global ctx
        # Drawing Heuristics
        x, y = agent.graph[node].position
        ctx.font = "13px Arial"
        ctx.fillStyle = 'black'
        ctx.fillText(agent.graph[node].heuristics,  x, y + 14)

    def draw_circle(node):
        global ctx, border
        if node_selected:
            if selected_node_ == node:
                border = 'selected'
            else:
                border = 'unselected'
        else:
                border = 'unselected'

        # Drawing circle shape
        x, y = agent.graph[node].position
        ctx.beginPath()
        ctx.strokeStyle = colors_for_border[border] # unselected -> black, selected -> red
        ctx.arc(x,y, radius, 0, 2 * javascript.Math.PI) # start angle (0), end angle (2 pi)
        ctx.fillStyle = colors_to_fill_inside[node_type]
        node_type = 'normal' # Node type is changed. If goal node --> green, If start node --> orange, If normal node --> white
        ctx.fill()
        ctx.stroke()
        
        # Drawing node name
        ctx.fillStyle = 'black'
        ctx.font = "20px Arial"
        ctx.textBaseline = "middle"
        ctx.fillText(node, x, y - 5)


        draw_heuristics(node)

    def draw_edges(node1, node2, flag=0):
        global ctx
        x1, y1 = agent.graph[node1].position
        x2, y2 = agent.graph[node2].position

        ctx.beginPath()
        if flag == 0:
            ctx.strokeStyle = 'black' 
            ctx.lineWidth = 1
        else:
            ctx.strokeStyle = 'red' 
            ctx.lineWidth = 5
        ctx.moveTo(x1,y1)
        ctx.lineTo(x2,y2)
        ctx.stroke()
        ctx.lineWidth = 1
        if flag == 1:
            draw_weights(node1, node2)
    
    def animate_graph():
        global node_type, val, selected_algorithm
        if (selected_algorithm not in ['bfs', 'dfs']):
            val = val[1:]
        start = val[0]
        for node in val[1:]:
            end = node
            print("start : ",start,"End : ",end)
            draw_edges(start, end, 1)
            start = end
        for circle_node in agent.graph.keys():
            if agent.start == circle_node:
                node_type = 'start'
            elif agent.goal == circle_node:
                node_type = 'goal'
            else:
                node_type = 'normal'
            draw_circle(circle_node)

    if any_change:
        ctx.clearRect(0, 0, document['canvas'].offsetWidth, document['canvas'].offsetHeight)

        #alert("inside update graph")
        visited = []
        for node in agent.graph.keys():
            if (node == agent.goal):
                node_type = 'goal'
            elif (node == agent.start):
                node_type = 'start'
            else:
                node_type = 'normal'
            
            children = agent.graph[node].children
            for child_node ,weight in children.items():
                if (node, child_node) in visited or (child_node, node) in visited:
                    continue
                visited.append((node, child_node))

                draw_edges(node, child_node)
                draw_weights(node, child_node)
            draw_circle(node)
        
        if animate:
            animate_graph()
            animate = False

        any_change = False
    if agent.status == 'searching':
        window.setTimeout(agent_search, 24)
    
    

def solve(algo):
    global agent, yield_result, any_change, result, i
    document["paragh"].innerText = "Solving"
    agent.status = 'searching'
    i = 0
    result = map_algorithm[algo]()
    if (result == None):
        document["paragh"].innerText = "Can't find"
        agent.status = 'idle'
        return
    
    update_graph()

    
def next_iteration():
    global yield_result, val
    val = next(yield_result)

def agent_search():
    global any_change, start_time, animate, selected_algorithm, result, val, i, j
    set_speed()
    if agent.status == 'searching':
        #if selected_algorithm == 'dfs':
        Len = len(result)
        if (i == Len):
            document["paragh"].innerText = "Solved"
            agent.status = 'idle'
            return 
        now_time = javascript.Date.now()
        if (now_time - start_time >= speed):
            val = result[i]
            i += 1
            any_change = True
            animate = True
            window.setTimeout(update_graph, 10)
            start_time = now_time
        else:
            window.setTimeout(update_graph, 10)
            
def graph_setup(event):
    global tool, counter, any_change, node_selected, selected_node_, From, To, node_heur
    def find_edge_ends(radius): # Finding edge ends to update weight of that edge
        visited = []
        for node in agent.graph.values():
            children = node.children
            x1,y1 = node.position
            for child_node in children.keys():
                
                if (node, child_node) in visited or (child_node, node) in visited:
                    continue
                visited.append((node,child_node))
                x2,y2 = agent.graph[child_node].position
                mid_x, mid_y = (x1 + x2)/2, (y1 + y2)/2
                if x <= mid_x + radius and x >= mid_x - radius and \
                    y <= mid_y + radius and y >= mid_y - radius:
                    
                    return node.name ,child_node
        return -1,-1
    def find_node():
        for node in agent.graph.values():
            if x <= node.position[0] + radius and x >= node.position[0] - radius and \
                    y <= node.position[1] + radius and y >= node.position[1] - radius:
                return node.name
        return -1

    # x and y co-ordinates
    x = event.clientX
    y = event.clientY
    x = x - canvas.offsetLeft
    y = y - canvas.offsetTop
    node_name = find_node()
    if node_name == -1:
        if tool == "nodeAdd":
            ctx.textAlign = "center"

            # Drawing node name
            ctx.fillStyle = 'black'
            ctx.font = "20px Arial"
            ctx.textBaseline = "middle"
            node_name = chr(counter%26 + 65)
            ctx.fillText(node_name, x, y - 5)

            # Creating actual node in graph
            agent.graph[node_name] = Node(node_name, position = (x, y))

            # Drawing Heuristics        
            ctx.font = "13px Arial"
            ctx.fillText("1",  x, y + 14)

            # Updating graph
            any_change = True
            counter += 1

        elif tool == "weights":
            From , To = find_edge_ends(radius)
            if From != -1: # i.e if the user clicked on the proper location in between any two nodes
                DialogBoxVisibility(True)
        
        # Making Changes
        update_graph()
    else:
            
        if tool == "nodeDelete":
            # Setting goal and agent to none, if that respective node is deleted.
            if agent.goal == node_name:
                agent.goal = None
            elif agent.start == node_name:
                agent.start = None

            # Deleting node's children
            for child in agent.graph[node_name].children.keys():
                del agent.graph[child].children[node_name]

            # Deleting node itself
            del agent.graph[node_name]

            # Updating graph
            any_change = True


        elif tool == "edgeAdd":
            if not node_selected:
                node_selected = True
                selected_node_ = node_name
                From = node_name

                # Updating graph to border out selected graph as red
                any_change = True

            
            elif node_selected:
                From = selected_node_
                To = node_name

                if From == To:
                    node_selected = False

                    # To remove red border
                    any_change = True


                # To avoid edge drawing redundantly over already existing edge
                elif To in agent.graph[From].children.keys() or To in agent.graph[To].children.keys():
                    node_selected = False

                    # To remove red border
                    any_change = True


                else :
                    x1,y1 = agent.graph[From].position
                    x2,y2 = agent.graph[To].position
                    
                    ctx.fillStyle = 'black'
                    
                    # Drawing Edge line
                    ctx.beginPath()
                    ctx.moveTo(x1,y1)
                    ctx.lineTo(x2,y2)
                    ctx.stroke()

                    # Drawing Default weight on edges
                    ctx.font = "18px Arial"
                    ctx.fillText(1,(x1+x2)/2, (y1+y2)/2)

                    # Updating edge weight in children of both nodes
                    agent.graph[From].children.update({To : 1})
                    agent.graph[To].children.update({From : 1})

                    node_selected = False

                    # To remove red border and update edges
                    any_change = True

                    
        elif tool == "edgeDelete":
            if not node_selected:
                node_selected = True
                selected_node_ = node_name
                From = node_name

                # Updating graph to border out selected node as red
                any_change = True


            elif node_selected:
                From = selected_node_
                To = node_name
            
                # If To Node is a child of From node then only delete 
                if To in agent.graph[From].children.keys():
                    del agent.graph[From].children[To]
                    del agent.graph[To].children[From]

                node_selected = False

                # To remove red border of selected node
                any_change = True


        elif tool == "heuristics":
            node_heur = node_name
            DialogBoxVisibility(True)

        

        elif tool == "setgoal":
            if node_name != agent.start: # To avoid setting both start and end as goal

                agent.goal = node_name 
                # To update goal node color
                any_change = True


        elif tool == "setstart":
            if node_name != agent.goal: # To avoid setting both start and end as goal
                agent.start = node_name 

                # To update start node color
                any_change = True

        # if any_change is set to True, graph will be erased and redrawn with changes
        update_graph()
  
def DialogBoxVisibility(value):
    global any_change
    if value:
        document["weights-modal"].showModal()
    else:
        document["weights-modal"].close()
        any_change = True
        update_graph()

def weightsUpdate():
    global any_change
    validated = document["weights-form"].reportValidity()
    if validated:
        result = document["weights-input"].value
        agent.graph[From].children.update({To: result})
        agent.graph[To].children.update({From: result})
        

def heuristicsUpdate():
    global any_change
    validated = document["weights-form"].reportValidity()
    if validated:
        result = document["weights-input"].value
        agent.graph[node_heur].heuristics = result
        any_change = True

def tool_select(do):
    global tool

    if do == "nodeAdd":
        document["paragh"].innerText = "Click to Add Node"
    elif do == "nodeDelete":
        document["paragh"].innerText = "Select Node to Delete"
    elif do == "edgeAdd":
        document["paragh"].innerText = "Select two nodes to add edge"
    elif do == "edgeDelete":
        document["paragh"].innerText = "Select two nodes to delete edge"
    elif do == "heuristics":
        document["paragh"].innerText = "Select node to modify heuristics"
    elif do == "weights":
        document["paragh"].innerText = "Click on respective weight to modify weights"
    elif do == "setstart":
        document["paragh"].innerText = "Select node as Start Node"
    elif do == "setgoal":
        document["paragh"].innerText = "Select node as Goal Node"    
    
    tool = do

def algo_select(algo):
    global selected_algorithm
    if algo == "bfs":
        document["paragh"].innerText = "Selected Breadth first search"
    elif algo == "dfs":
        document["paragh"].innerText = "Selected Depth first search"
    elif algo == "hc":
        document["paragh"].innerText = "Selected Hill climbing"
    elif algo == "bs":
        document["paragh"].innerText = "Selected Beam search"
    elif algo == "bb":
        document["paragh"].innerText = "Selected Branch and bound"
    elif algo == "bb-h":
        document["paragh"].innerText = "Selected Branch and bound + additional heuristics"
    elif algo == "astar":
        document["paragh"].innerText = "Selected A Star"
    elif algo == "oracle":
        document["paragh"].innerText = "Selected oracle"
    elif algo == "oracleel":
        document["paragh"].innerText = "Selected oracle with extended lists"
    elif algo == "bestfs":
        document["paragh"].innerText = "Selected Best First Search"
    elif algo == "aostar":
        document["paragh"].innerText = "Selected AO Star"
    elif algo == "bb-el":
        document["paragh"].innerText = "Selected Branch and Bound with extended lists"

    selected_algorithm = algo

def saved_graph():
    global any_change, agent, counter
    graph = int(document['Select'].value)
    
    if graph == 1:
        #alert("inside 1")
        agent.graph, c = G1()
    elif graph == 2:
        #alert("inside 2")
        agent.graph, c = G2()

    counter = c 
    any_change = True
    update_graph()

def update_canvas_size():
    inner = document['right']
    canvas.setAttribute('width', str(inner.offsetWidth));
    canvas.setAttribute('height',str(inner.offsetHeight));

def set_speed():
    global speed
    value = document['Speed'].value
    if value == '2x':
        speed = 200
    elif value == '1.5x':
        speed = 600
    else:
        speed = 800
    #alert(speed)


canvas = document["canvas"]
ctx = canvas.getContext("2d")
window_width = window.innerWidth
window_height = window.innerHeight

canvas.setAttribute('width', str(document['right'].offsetWidth));
canvas.setAttribute('height',str(document['right'].offsetHeight));

node_type = 'normal' 
border = 'unselected'
colors_to_fill_inside = {'goal' : "green", 'normal' : 'white', 'start': 'orange'}
colors_to_fill_text = {'goal' : 'white', 'normal' : 'black', 'start':'black'}
colors_for_border = {'selected' : 'red', 'unselected' : 'black'}

tool = None
selected_algorithm = None

counter = 0
node_name = chr(counter + 65)
radius = 20

# On clicking , if any node is selected
node_selected = False

# selected node
selected_node_ = None

# keeping track of change
any_change = False
animate = False

# variable to hold iterator of yield and individual yielded value
yield_result = None
result = None
val = None
node_heur = None
i = 0; j = 0

# For edge manipulation - Adding and deleting
From = None
To = None

# set speed
speed = 800


agent = SearchAgent()
map_algorithm = {'bfs' : agent.bfs, 'dfs' : agent.dfs , 'hc' : agent.hc \
    ,'bs' : agent.bs, 'bb' : agent.bb, 'bb-h' : agent.bb_h, 'astar' : agent.bfs,'oracle' : agent.bs,'bestfs' : agent.bs,'oracleel' : agent.bfs }


# Selecting Tools
document['nodeAdd'].bind('click', lambda e: tool_select('nodeAdd'))
document['nodeDelete'].bind('click', lambda e: tool_select('nodeDelete'))
document['edgeAdd'].bind('click', lambda e: tool_select('edgeAdd'))
document['edgeDelete'].bind('click', lambda e: tool_select('edgeDelete'))
document['heuristics'].bind('click', lambda e: tool_select('heuristics'))
document['weights'].bind('click', lambda e: tool_select('weights'))

# For Adjusting Weights and heuristics
document["weights-close"].bind("click", lambda e: DialogBoxVisibility(False))
document["weights-update"].bind("click", lambda e:  weightsUpdate() if tool == 'weights' else heuristicsUpdate())

# For setting goal and start
document['setgoal'].bind('click', lambda e: tool_select('setgoal'))
document['setstart'].bind('click', lambda e: tool_select('setstart'))

# For choosing Algorithm
document['dfs'].bind('click', lambda e: algo_select('dfs'))
document['bfs'].bind('click', lambda e: algo_select('bfs'))
document['hc'].bind('click', lambda e: algo_select('hc'))
document['bs'].bind('click', lambda e: algo_select('bs'))
document['bb'].bind('click', lambda e: algo_select('bs'))
document['bb-h'].bind('click', lambda e: algo_select('bfs'))
document['astar'].bind('click', lambda e: algo_select('bfs'))
document['oracle'].bind('click', lambda e: algo_select('bs'))
document['bestfs'].bind('click', lambda e: algo_select('bs'))
document['oracleel'].bind('click', lambda e: algo_select('bfs'))
document['bb-el'].bind('click', lambda e: algo_select('bs'))
document['aostar'].bind('click', lambda e: algo_select('bfs'))


# To solve the graph
document['solve'].bind('click', lambda e: solve(selected_algorithm))

# To set up graph -> Node creation, node deletion, edge creation, edge deletion
document['canvas'].bind('mousedown', lambda e: graph_setup(e))

document["Select"].bind('change', lambda e: saved_graph())

document["Speed"].bind('change', lambda e: set_speed())


# Keeping track of start time to use while animating the graph in proper interval
start_time = javascript.Date.now()
