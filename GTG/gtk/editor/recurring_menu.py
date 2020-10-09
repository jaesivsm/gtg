from gettext import gettext as _
from datetime import datetime
class RecurringMenu():
    """ RecurringMenu provides a simple layer of abstraction
    for the menu where the user enables a task to be repeating
    """
    PREFIX = _('Every ')

    def __init__(self, requester, tid, builder):
        # General attributes
        self.task = requester.get_task(tid)
        self.selected_recurring_term = self.task.get_recurring_term()
        
        # Getting the necessary Gtk objects
        self.title = builder.get_object("title_label")
        self.title_separator = builder.get_object("title_separator")
        self.repeat_button = builder.get_object("repeat_checkbutton")
        self.repeat_icon = builder.get_object("repeat_icon")
        self.icon_style = self.repeat_icon.get_style_context()
        self.stack = builder.get_object("main_stack")
        self.page1 = builder.get_object("stack_main_box")

        # Update the editor using the task recurring status
        self.update_header()
        self.repeat_button.set_active(self.task.get_recurring())
        if self.task.get_recurring():
            self.icon_style.add_class('recurring-active')

    def update_repeat_button(self, active=True):
        """ Update the icon color of the repeat-menu-button in the task editor """
        if active:
            self.icon_style.add_class('recurring-active')
        else:
            self.icon_style.remove_class('recurring-active')

    def is_term_set(self):
        return self.selected_recurring_term is not None

    def set_selected_term(self, string):
        self.selected_recurring_term = string

    def update_tick(self):
        """
        Update the task object recurring status and all indicators
        according to the repeat-checkbox-button status
        """
        if self.repeat_button.get_active():
            if not self.is_term_set():
                self.set_selected_term('day')
            self.update_term()
            self.update_repeat_button()
        else:
            self.update_task(False)
            self.update_repeat_button(active=False)

    def update_term(self):
        """
        Update the header and the task object(only if the repeat-checkbutton is checked)
        when a new term was selected
        """
        if self.repeat_button.get_active():
            self.update_task(True)
        self.update_header()

    def update_task(self, enable=True):
        """ Updates the task object """
        if enable:
            self.task.set_recurring(enable, self.selected_recurring_term, newtask=True)
        else:
            self.task.set_recurring(enable)
            
    def update_header(self):
        """ Updates the header anytime a term is selected """
        formated_term = self.selected_recurring_term
        if self.is_term_set():
            if formated_term.isdigit():
                if len(formated_term) <= 2 :
                    day = datetime.strptime(f'{formated_term}', '%d').strftime('%d')
                    formated_term = _('{day} of the Month')
                    formated_term = formated_term.format(day=day)
                else:
                    formated_term = datetime.strptime(f'{formated_term[:2:]}-{formated_term[2::]}', '%m-%d').strftime('%B %d')
            elif formated_term == 'week':
                formated_term = datetime.today().strftime('%A')
            elif formated_term == 'month':
                formated_term = _('{day} of the Month')
                formated_term = formated_term.format(day=datetime.today().strftime('%d'))
            elif formated_term == 'year':
                formated_term = datetime.today().strftime('%B %d')
            self.title.show()
            self.title_separator.show()
            self.title.set_markup(f"{RecurringMenu.PREFIX}<b>{formated_term}</b>")
        else:
            self.title.hide()
            self.title_separator.hide()
    
    def reset_stack(self):
        """ Reset popup stack to the first page """
        self.stack.set_transition_duration(0)
        self.stack.set_visible_child(self.page1)
        self.stack.set_transition_duration(200)