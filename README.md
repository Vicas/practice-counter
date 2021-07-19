# practice-counter
A small app for tracking your success/failure rate while practicing something

To customize button names/count/hotkeys, edit the file `config.ini`. To add an entirely new button, add new name to the `buttons` list under `[SETTINGS]` and then add a new section with the same name under `[BUTTON2]`

Settings:
[SETTINGS]
`counter_name` - Name at the top of the practice counter
`buttons` - List of button names, comma-separated. Each name here must have a section below in the config, to set that particular button

[BUTTON-SPECIFIC SETTINGS]
`label` - Name on the button
`hotkey` - Button on your keyboard to press to increment this button in the app
`success` - Whether events on this button should be considered successes or failures, for percentage reporting
`color` - Color of the button. Can either be a hex value or any Tkinter-valid color name
