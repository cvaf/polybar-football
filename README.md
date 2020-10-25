# Polybar - United Fixtures

A polybar display with Manchester United's next fixture.

![](imgs/example.png)


### Usage:
1. Update the shebang to point to your venv. 
2. Change the team name :(
3. Add the following to your polybar config:

```
[module/manutd-fixtures]
type = custom/script

interval = 86400
format-background = ${color.mf}
format-foreground = ${color.fg}
exec = "python path/to/manutd_fixtures.py"
```
