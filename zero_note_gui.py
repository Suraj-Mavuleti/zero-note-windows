import sys
import gi
import os
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango

CONFIG_DIR = os.path.expanduser("~/.config/zero-note")
VAULT_FILE = os.path.join(CONFIG_DIR, "vault.json")

class ZeroNote(Gtk.Window):
    def __init__(self):
        super().__init__(title="Zero Note - Ultimate Studio")
        self.set_default_size(1250, 800)
        
        os.makedirs(CONFIG_DIR, exist_ok=True)
        self.notes = self.load_vault()
        
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = ""
        self.header.get_style_context().add_class("hidden-header")
        self.set_titlebar(self.header)
        
        self.setup_css()
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(main_box)
        
        # ================= SIDEBAR (Vault) =================
        self.sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.sidebar.set_size_request(260, -1)
        self.sidebar.get_style_context().add_class("sidebar")
        main_box.pack_start(self.sidebar, False, False, 0)
        
        logo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        logo = Gtk.Label(label="Z E R O N O T E")
        logo.get_style_context().add_class("sidebar-logo")
        logo_box.pack_start(logo, True, True, 0)
        self.sidebar.pack_start(logo_box, False, False, 20)
        
        btn_new = Gtk.Button(label="📝 New Note")
        btn_new.get_style_context().add_class("action-btn")
        btn_new.connect("clicked", self.create_new_note)
        self.sidebar.pack_start(btn_new, False, False, 10)
        
        lbl_vault = Gtk.Label(label="PERSONAL VAULT")
        lbl_vault.get_style_context().add_class("section-label")
        lbl_vault.set_halign(Gtk.Align.START)
        lbl_vault.set_margin_start(20)
        lbl_vault.set_margin_top(10)
        self.sidebar.pack_start(lbl_vault, False, False, 10)
        
        scroll_sidebar = Gtk.ScrolledWindow()
        scroll_sidebar.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.notes_list = Gtk.ListBox()
        self.notes_list.get_style_context().add_class("transparent-list")
        self.notes_list.connect("row-selected", self.on_note_selected)
        scroll_sidebar.add(self.notes_list)
        self.sidebar.pack_start(scroll_sidebar, True, True, 0)
        
        self.refresh_notes_list()
        
        tools_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        tools_box.set_margin_start(15)
        tools_box.set_margin_end(15)
        tools_box.set_margin_bottom(15)
        
        btn_graph = Gtk.Button(label="🕸️ Graph")
        btn_graph.get_style_context().add_class("nav-btn")
        btn_sync = Gtk.Button(label="☁️ Sync")
        btn_sync.get_style_context().add_class("nav-btn")
        tools_box.pack_start(btn_graph, True, True, 0)
        tools_box.pack_start(btn_sync, True, True, 0)
        self.sidebar.pack_end(tools_box, False, False, 0)
        
        # ================= WORKSPACE =================
        self.workspace = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.workspace.get_style_context().add_class("workspace-bg")
        main_box.pack_start(self.workspace, True, True, 0)
        
        # Toolbar
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        toolbar.get_style_context().add_class("toolbar")
        
        self.title_entry = Gtk.Entry()
        self.title_entry.set_placeholder_text("Untitled Note")
        self.title_entry.get_style_context().add_class("title-entry")
        toolbar.pack_start(self.title_entry, True, True, 0)
        
        btn_save = Gtk.Button(label="💾 Save")
        btn_save.get_style_context().add_class("nav-btn")
        btn_save.connect("clicked", self.save_current_note)
        toolbar.pack_start(btn_save, False, False, 0)
        
        btn_del = Gtk.Button(label="🗑️")
        btn_del.get_style_context().add_class("nav-btn")
        btn_del.connect("clicked", self.delete_current_note)
        toolbar.pack_start(btn_del, False, False, 0)
        
        self.workspace.pack_start(toolbar, False, False, 0)
        
        # Editor
        scroll_editor = Gtk.ScrolledWindow()
        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textview.set_left_margin(40)
        self.textview.set_right_margin(40)
        self.textview.set_top_margin(20)
        self.textview.set_bottom_margin(20)
        self.textview.get_style_context().add_class("note-editor")
        self.textview.modify_font(Pango.FontDescription('sans-serif 16'))
        
        scroll_editor.add(self.textview)
        self.workspace.pack_start(scroll_editor, True, True, 0)
        
        self.current_note_id = None
        if self.notes:
            self.load_note_into_editor(list(self.notes.keys())[0])

    def load_vault(self):
        try:
            if os.path.exists(VAULT_FILE):
                with open(VAULT_FILE, "r") as f: return json.load(f)
        except: pass
        return {"1": {"title": "Welcome to Zero Note", "content": "The ultimate privacy-first premium note taking application.\n\n- Markdown Support\n- Infinite Canvas\n- End-to-End Encryption"}}

    def save_vault(self):
        with open(VAULT_FILE, "w") as f: json.dump(self.notes, f)

    def refresh_notes_list(self):
        for child in self.notes_list.get_children():
            self.notes_list.remove(child)
            
        for nid, data in self.notes.items():
            row = Gtk.ListBoxRow()
            row.get_style_context().add_class("note-row")
            row.note_id = nid
            
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            lbl = Gtk.Label(label=data.get("title", "Untitled"))
            lbl.set_halign(Gtk.Align.START)
            lbl.set_margin_start(15)
            lbl.set_margin_top(10)
            lbl.set_margin_bottom(10)
            lbl.get_style_context().add_class("note-title-lbl")
            box.pack_start(lbl, True, True, 0)
            row.add(box)
            self.notes_list.add(row)
        self.notes_list.show_all()

    def load_note_into_editor(self, nid):
        if nid in self.notes:
            self.current_note_id = nid
            self.title_entry.set_text(self.notes[nid].get("title", ""))
            self.textview.get_buffer().set_text(self.notes[nid].get("content", ""))

    def on_note_selected(self, listbox, row):
        if row: self.load_note_into_editor(row.note_id)

    def save_current_note(self, widget):
        if not self.current_note_id:
            self.current_note_id = str(len(self.notes) + 1)
            self.notes[self.current_note_id] = {}
            
        self.notes[self.current_note_id]["title"] = self.title_entry.get_text()
        buf = self.textview.get_buffer()
        self.notes[self.current_note_id]["content"] = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        self.save_vault()
        self.refresh_notes_list()

    def create_new_note(self, widget):
        self.current_note_id = str(len(self.notes) + 1)
        self.notes[self.current_note_id] = {"title": "New Note", "content": ""}
        self.save_vault()
        self.refresh_notes_list()
        self.load_note_into_editor(self.current_note_id)

    def delete_current_note(self, widget):
        if self.current_note_id and self.current_note_id in self.notes:
            del self.notes[self.current_note_id]
            self.save_vault()
            self.refresh_notes_list()
            self.current_note_id = None
            self.title_entry.set_text("")
            self.textview.get_buffer().set_text("")

    def setup_css(self):
        css = b'''
            window { background-color: #030305; }
            .hidden-header { background: #030305; min-height: 0px; padding: 0px; border: none; box-shadow: none; }
            .sidebar { background-color: rgba(10, 12, 18, 0.98); border-right: 1px solid rgba(255, 255, 255, 0.05); }
            .sidebar-logo { color: #FFFFFF; font-size: 20px; font-weight: 900; letter-spacing: 5px; text-shadow: 0 0 15px rgba(0, 255, 170, 0.6); }
            .action-btn { background: linear-gradient(45deg, #00FFaa, #00b377); color: #000000; border-radius: 12px; font-weight: bold; padding: 12px; margin: 0 15px; border: none; box-shadow: 0 5px 15px rgba(0, 255, 170, 0.3); transition: all 0.3s; }
            .action-btn:hover { box-shadow: 0 8px 25px rgba(0, 255, 170, 0.5); }
            .section-label { color: #4A5568; font-size: 11px; font-weight: 900; letter-spacing: 2px; }
            .transparent-list { background: transparent; }
            .note-row { background: transparent; border-radius: 8px; margin: 2px 10px; border: 1px solid transparent; }
            .note-row:hover { background: rgba(255, 255, 255, 0.05); cursor: pointer; }
            .note-row:selected { background: rgba(0, 255, 170, 0.1); border-left: 3px solid #00FFaa; }
            .note-title-lbl { color: #c9d1d9; font-weight: bold; font-size: 14px; }
            .nav-btn { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); color: #8B94A5; border-radius: 10px; padding: 8px 15px; font-weight: bold; font-size: 13px; transition: all 0.2s ease; }
            .nav-btn:hover { background: rgba(0, 255, 170, 0.1); color: #00FFaa; border: 1px solid #00FFaa; box-shadow: 0 0 15px rgba(0, 255, 170, 0.2); }
            .workspace-bg { background: #050608; }
            .toolbar { background: #080a0f; padding: 15px 30px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
            .title-entry { background: transparent; color: #FFFFFF; font-size: 24px; font-weight: bold; border: none; box-shadow: none; caret-color: #00FFaa; }
            .title-entry:focus { border: none; box-shadow: none; }
            .note-editor { background: transparent; color: #e6edf3; caret-color: #00FFaa; line-height: 1.6; }
            .note-editor text { background: transparent; }
        '''
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == "__main__":
    win = ZeroNote()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
