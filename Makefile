init:
	@echo "\
from models import LineID, Stop\n\
\n\
key = \"\"\n\
stops = [\n\
  Stop(LineID.L, \"L10N\", 8),\n\
  Stop(LineID.J, \"M16S\", 6),\n\
  Stop(LineID.G, \"G30S\", 8),\n\
  Stop(LineID.L, \"L10S\", 8),\n\
  Stop(LineID.G, \"G30N\", 8),\n\
]\
" > platform3/config.py
	@echo "Please add your API key to platform3/config.py"
	pip install -r requirements.txt
