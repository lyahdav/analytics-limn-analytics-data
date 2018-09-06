# Usage
```
 ./analytics/phab-stats --project-id <projectID>
```
- Generates output.csv file with team and individual velocities
- Tasks without estimates are treated as 0 points
- pass in `--task-counts` to ignore points and only calculate task counts
- pass in `--task-counts-and-points` argument to calculate task counts and point counts

# Install python libs

```
sudo pip  install -r ./requirements.txt
```
If lxml gives trouble, uninstall and install again.

