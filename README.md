# Ticket printer
NETIO Products project for access to thermal-label printers.

# Usage
## CLI

### Capturing new label
you can either save the label into the

To capture new label, spin up the fake-printer service

```bash
cd Printer
python3 FakePrinter.py -o /tmp/data
```

Start up the application for label printing


### Sending label into the printer
Now that you've captured the label, you can use the command line to print the label.

```bash
python3 Printer.py localhost /tmp/data/
```

## Programmatically



# Note
please excuse this horrible creation i wrote when i had no idea what i'm doing(not that it's better now lol).
I would not let it see a daylight if i was not paid to do it.
