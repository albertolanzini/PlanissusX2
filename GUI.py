import wx
from wx.lib.pubsub import pub

from gridVisualization import *

class MainFrame(wx.Frame):
    def __init__(self, visualizer):
        wx.Frame.__init__(self, None, title="Main Frame")
        panel = wx.Panel(self)

        interactive_button = wx.Button(panel, label="Interactive Mode")
        interactive_button.Bind(wx.EVT_BUTTON, self.on_interactive_mode)

        automatic_button = wx.Button(panel, label="Automatic Mode")
        automatic_button.Bind(wx.EVT_BUTTON, self.on_automatic_mode)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(interactive_button, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(automatic_button, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(sizer)
        self.visualizer = visualizer

    def on_interactive_mode(self, event):
        self.visualizer.visualize(interactive=True, delay = 0)

    def on_automatic_mode(self, event):
        # You can replace this with your desired number of days
        delay = 0.06  # You can replace this with your desired delay
        self.visualizer.visualize(interactive=False, delay=delay)