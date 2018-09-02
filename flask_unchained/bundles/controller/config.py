class Config:
    """
    Default configuration options for the controller bundle.
    """

    FLASH_MESSAGES = True
    """
    Whether or not to enable flash messages. 
    
    NOTE: This only works for messages flashed using the
    :meth:`flask_unchained.Controller.flash` method;
    using the :func:`flask.flash` function directly will not respect this setting.
    """
