import wx
from wx.lib.pubsub import pub

from gridVisualization import *

class MainFrame(wx.Frame):
    def __init__(self, visualizer):
        wx.Frame.__init__(self, None, title="Choose Wisely!")
        panel = wx.Panel(self)

        interactive_button = wx.Button(panel, label="Interactive Mode", size=(200, 50))
        interactive_button.SetBackgroundColour('purple')
        interactive_button.SetForegroundColour('white')
        interactive_button.Bind(wx.EVT_BUTTON, self.on_interactive_mode)

        automatic_button = wx.Button(panel, label="Automatic Mode", size=(200, 50))
        automatic_button.SetBackgroundColour('red')
        automatic_button.SetForegroundColour('white')
        automatic_button.Bind(wx.EVT_BUTTON, self.on_automatic_mode)

        mode_text = wx.StaticText(panel, label="Choose Automatic mode for a more dynamic experience,\nchoose Interactive mode for a deeper analysis of the ecosystem.")
        font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        mode_text.SetFont(font)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(interactive_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(automatic_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(mode_text, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(sizer)
        self.visualizer = visualizer

    def on_interactive_mode(self, event):
        self.visualizer.visualize(interactive=True, delay = 0)

    def on_automatic_mode(self, event):
        # You can replace this with your desired number of days
        delay = 0.25  # You can replace this with your desired delay
        self.visualizer.visualize(interactive=False, delay=delay)