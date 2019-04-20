# namespacing class objects to be used as common resources accross modules
# these are effectively singletons for the game engine
# must be properly initialized ONLY in the main script

settings = None
core = None
display = None
clock = None
events = None
