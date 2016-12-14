# -*- coding: utf-8 -*-
from ..query_manager.QueryManager import QueryManager

class ContextManager:
    def __init__(self, amazon_id, username):
        self.amazon_id = amazon_id
        self.username = username
        self.qm = QueryManager()

    def getContext(self, intent_obj):
        """
        Complete empty slots in the supplied intent object.
        Update context in database if necessary
        """
        # get latest context for a user
        # compare current intent obj with said context
        # fill in empty slots
        # determine if update is needed, and updateContext if yes
        context = self.retrieveContext()
        mixinContext(self, intent_obj, context)
        return intent_obj

    def retrieveContext(self):
        context = self.qm.getContext({"amazon_id":self.amazon_id})
        # assert context["amazon_id"] == self.amazon_id
        return context
        
    def mixinContext(self, intent_obj, context):
        """
        Fill in slots with info from context.
        Update the context if necessary
        """
        slots = intent_obj.getSlots()
        context_changed = False
        for k,v in slots:
            context_val = context.get(k, None)
            # fill in slots with context
            if v is None:
                intent_obj.setSlot(k, context_val) 
            else:# update context with current info
                context[k] = v
                context_changed = True
        if context_changed:
            updateContext(context)
            
    def updateContext(self, context):
        """
        update context info in database
        if there hasn't been any previous context for the user, add the current 
        slots as an entry for this user.
        """
        context["amazon_id"] = self.amazon_id
        context["username"] = self.username
        self.qm.updateContext(context)

if __name__ == "__main__":
    cm = ContextManager("test")
