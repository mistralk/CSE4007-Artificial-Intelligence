// HW1-3: A* Search
// Sohn Yunha

#include <iostream>
#include <queue>
#include <cmath>
#include <list>
#include <fstream>
#include <string>

using namespace std;

enum color { WHITE, GRAY, BLACK };
enum tyle { WALL = 1, ROAD, START, GOAL, PATH };
color is_visited[501][501] = { WHITE };

int maze[501][501];
int length, _time;
int m, n;

class Node {
public:
	int y;
	int x;
	int accum;			// distance (start node ~ this node)
	float evaluation;	// accum + distance to goal
	list<pair<int, int>> path;

	Node() {
	}

	bool operator()(const Node* lhs, const Node* rhs) const {
		return lhs->evaluation > rhs->evaluation;
	}
};

priority_queue<Node*, vector<Node*>, Node> discovered_nodes;
vector<pair<int, int>> goals;

float heuristic(int y, int x) {
	
	float ret = 123456789.0; // any big big value
	for (auto goal : goals) {
		float h = abs(goal.first - y) + abs(goal.second - x);
//		float h = (float)sqrt((goal.first - y) * (goal.first - y) + (goal.second - x) * (goal.second - x));
		if (ret > h)
			ret = h;
	}
	return ret;
}

Node* make_child_node(Node *present_node, int dy, int dx) {
	Node* n = new Node;

	n->y = present_node->y + dy;
	n->x = present_node->x + dx;
	n->accum = present_node->accum + 1;
	n->evaluation = n->accum + heuristic(n->y, n->x);
	n->path = present_node->path;
	n->path.push_back(make_pair(n->y,n->x));
//	cout << "child: " << n->y << "," << n->x << " " << n->accum << "+" << heuristic(n->y, n->x) << endl;

	return n;
}

int main() {
	ifstream input;
	ofstream output;
	string file_path;
	getline(cin, file_path);
	input.open(file_path + "\\input.txt");
	output.open(file_path + "\\output.txt");

	Node* start_node = new Node;

	input >> m >> n;

	for (int i = 0; i < m; ++i) {
		for (int j = 0; j < n; ++j) {

			input >> maze[i][j];
			if (maze[i][j] == START) {
				start_node->y = i;
				start_node->x = j;
				start_node->evaluation = 0;
				start_node->accum = 0;
			}
			else if (maze[i][j] == GOAL) {
				goals.push_back(make_pair(i, j));
			}
		}
	}

	discovered_nodes.push(start_node);

	Node* goal_node = nullptr;
	int found = 0;

	while (!discovered_nodes.empty()) {

		Node* present = discovered_nodes.top();

		int y = present->y;
		int x = present->x;

//		cout << y << "," << x << " " << present->evaluation << endl;

		if (maze[y][x] == GOAL) {
			goal_node = discovered_nodes.top();
			break;
		}

		++_time;
		is_visited[y][x] = BLACK;

		discovered_nodes.pop();

		if (y > 0 && maze[y - 1][x] != WALL && !is_visited[y-1][x])
			discovered_nodes.push(make_child_node(present, -1, 0));
		if (y < m - 1 && maze[y + 1][x] != WALL && !is_visited[y + 1][x])
			discovered_nodes.push(make_child_node(present, +1, 0));
		if (x > 0 && maze[y][x - 1] != WALL && !is_visited[y][x - 1])
			discovered_nodes.push(make_child_node(present, 0, -1));
		if (x < n - 1 && maze[y][x + 1] != WALL && !is_visited[y][x + 1])
			discovered_nodes.push(make_child_node(present, 0, +1));

		delete present;
	}

	if (goal_node != nullptr) {
		goal_node->path.pop_back();

		for (auto l : goal_node->path)
			maze[l.first][l.second] = PATH;

		for (int i = 0; i < m; ++i) {
			for (int j = 0; j < n; ++j) {
				output << maze[i][j] << " ";
			}
			output << endl;
		}
		output << "---\nlength=" << goal_node->path.size() << "\ntime=" << _time << endl;
	}

	input.close();
	output.close();

	return 0;
}