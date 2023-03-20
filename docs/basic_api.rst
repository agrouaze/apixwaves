#############
API reference
#############

..
    to document functions, add them to __all__ in ../xsarslc/__init__.py

.. automodule:: xsarslc
    :members:


processing
==========

.. automodule:: xsarslc.processing.xspectra
    :members: compute_subswath_xspectra, compute_IW_subswath_intraburst_xspectra, compute_IW_subswath_interburst_xspectra, compute_modulation, compute_azimuth_cutoff,

.. automodule:: xsarslc.processing.intraburst
    :members: tile_burst_to_xspectra, compute_intraburst_xspectrum, compute_looks

.. automodule:: xsarslc.processing.interburst
    :members: compute_interburst_xspectrum, tile_bursts_overlap_to_xspectra

.. automodule:: xsarslc.burst
    :members: burst_valid_indexes, crop_burst, deramp_burst

..automodule:: xsarslc.processing.impulseResponse
    :members: compute_IWS_subswath_Impulse_Response, compute_WV_Impulse_Response
