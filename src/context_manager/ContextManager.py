# -*- coding: utf-8 -*-
from ..query_manager.QueryManager import QueryManager

class ContextManager:
    def __init__(self, amazon_id, username):
        #TODO: should context manager take both amazon_id and username here?
        #      did we previously pass access token as user(name)? 
        #      can we even get the user's username?
        self.amazon_id = amazon_id
        self.username = username
        self.qm = QueryManager()

    def getContext(self, intent_obj):
        """
        Complete empty slots in the supplied intent object.
        Update context in database if necessary
        """
        context = self.retrieveContext()
        self.mixinContext(intent_obj, context)
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
        for k,v in slots.iteritems():
            context_val = context.get(k, None)
            # fill in slots with context
            if v is None:
                intent_obj.setSlot(k, context_val) 
            else:# update context with current info
                context[k] = v
                context_changed = True
        if context_changed:
            self.updateContext(context)
            
    def updateContext(self, context):
        """
        update context info in database
        if there hasn't been any previous context for the user, add the current 
        slots as an entry for this user.
        """
        context["amazon_id"] = self.amazon_id
        # TODO: make sure we need both amazoin_id and username, if we only
        # need amazon_id, then delete the line below. 
        context["username"] = self.username
        self.qm.updateContext(context)

if __name__ == "__main__":
    cm = ContextManager("test")
