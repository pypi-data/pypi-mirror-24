import wx


class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(
            None,
            title='μOTP+',
            size=(320, 240),
            style=wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX,
        )

        wrapper = wx.Panel(self)
        sizer_wrapper = wx.BoxSizer(wx.VERTICAL)

        gauge_time = wx.Gauge(wrapper, range=30, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        gauge_time.SetValue(20)
        sizer_wrapper.Add(gauge_time, flag=wx.EXPAND)

        panel = wx.Panel(wrapper)
        box = wx.BoxSizer(wx.VERTICAL)

        txt_token = wx.TextCtrl(panel, style=wx.TE_READONLY | wx.TE_CENTRE | wx.BORDER_NONE)
        txt_token.SetFont(wx.Font(32, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        txt_token.SetLabelText('1234567')
        box.Add(txt_token, flag=wx.EXPAND)

        box.AddSpacer(60)

        label_serial = wx.StaticText(panel, label="S/N")
        box.Add(label_serial, flag=wx.ALIGN_CENTRE)

        box.AddSpacer(5)

        txt_serial = wx.TextCtrl(panel, style=wx.TE_READONLY | wx.TE_CENTRE | wx.BORDER_NONE)
        txt_serial.SetLabelText('1234-5678-9012')
        box.Add(txt_serial, flag=wx.ALIGN_CENTRE)

        panel.SetSizer(box)
        sizer_wrapper.Add(panel, proportion=1, flag=wx.ALL | wx.EXPAND, border=20)
        wrapper.SetSizer(sizer_wrapper)

        self.Centre()
        self.Show()

app = wx.App()
MainWindow()
app.MainLoop()
