// HW1-1: Iterative Deepening Search
// Sohn Yunha

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int maze[501][501];
int length, _time;
int m, n;
bool goal_visited;

ofstream output;

enum color { WHITE, GRAY, BLACK };
enum tyle { WALL = 1, ROAD, START, GOAL, PATH };

int DFS(int y, int x, int depth, int depth_limit, color is_visited[][501]) {

	if (goal_visited || depth > depth_limit || is_visited[y][x]) {
		return 0;
	}

	if (maze[y][x] == 4) {

		for (int i = 0; i < m; ++i) {
			for (int j = 0; j < n; ++j) {
				if (is_visited[i][j] == GRAY && maze[i][j] == ROAD) output << "5 ";
				else output << maze[i][j] << " ";
			}
			output << endl; 
		}
		output << "---\nlength=" << depth - 1 << "\ntime=" << _time << endl;
		goal_visited = true;
		return 1;
	}

	++_time;
	is_visited[y][x] = GRAY;

	if (y > 0 && maze[y - 1][x] != WALL)
		DFS(y - 1, x, depth + 1, depth_limit, is_visited);
	if (y < m-1 && maze[y + 1][x] != WALL)
		DFS(y + 1, x, depth + 1, depth_limit, is_visited);
	if (x > 0 && maze[y][x - 1] != WALL)
		DFS(y, x - 1, depth + 1, depth_limit, is_visited);
	if (x < n-1 && maze[y][x + 1] != WALL)
		DFS(y, x + 1, depth + 1, depth_limit, is_visited);

	is_visited[y][x] = BLACK;
	return 0;
}

int main() {
	int start_y;
	int start_x;

	ifstream input;

	string file_path;
	getline(cin, file_path);
	input.open(file_path + "\\input.txt");
	output.open(file_path + "\\output.txt");

	input >> m >> n;

	for (int i = 0; i < m; ++i) {
		for (int j = 0; j < n; ++j) {

			input >> maze[i][j];
			if (maze[i][j] == START) {
				start_y = i;
				start_x = j;
			}
		}
	}

	for (int depth_limit = 0; ; ++depth_limit) {
		color is_visited[501][501] = { WHITE };
		DFS(start_y, start_x, 0, depth_limit, is_visited);
		if (goal_visited)
			break;
	}

	input.close();
	output.close();

	return 0;
}