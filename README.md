A task tracking program that runs through the command line, accepts user inputs and stores them in a JSON file.

*The program stores data in a 'tasks.json' file found in the same directory the program is in
*If the program failes to find the file it will create it and display a message of avaliable commands to the user

Avaliable commands:
  add "description"            - Add a new task
  update <id> "new desc"       - Update task description
  delete <id>                  - Delete a task
  list                         - List all tasks
  list done|todo|in-progress   - Filter by status
  mark-done <id>               - Mark a task as done
  mark-in-progress <id>        - Mark a task as in-progress
  exit                         - Exit the program
