from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import ChoicePreference, StringPreference

# Sections
# --------
site = Section("site")


# Global Preferences
# ------------------
@global_preferences_registry.register
class SiteName(StringPreference):
    """Site Name"""

    name = "name"
    section = site
    default = "GEA"
    required = True


@global_preferences_registry.register
class SiteLogoPath(StringPreference):
    """Path to Logo in static"""

    name = "logo_path"
    section = site
    default = "gea.png"
    required = True


@global_preferences_registry.register
class SiteTheme(ChoicePreference):
    """Bootstrap compatible theme name (must be in static/css/bootstrap.<theme-name>.min.css)"""

    name = "theme"
    section = site
    default = "cosmo"
    required = False
    choices = [
        ("", "Bootstrap 5.3"),
        ("cerulean", "Bootswatch Cerulean"),
        ("cosmo", "Bootswatch Cosmo (DEFAULT)"),
        ("cyborg", "Bootswatch Cyborg"),
        ("darkly", "Bootswatch Darkly"),
        ("flatly", "Bootswatch Flatly"),
        ("journal", "Bootswatch Journal"),
        ("litera", "Bootswatch Litera"),
        ("lumen", "Bootswatch Lumen"),
        ("lux", "Bootswatch Lux"),
        ("materia", "Bootswatch Materia"),
        ("minty", "Bootswatch Minty"),
        ("pulse", "Bootswatch Pulse"),
        ("sandstone", "Bootswatch Sandstone"),
        ("simplex", "Bootswatch Simplex"),
        ("sketchy", "Bootswatch Sketchy"),
        ("slate", "Bootswatch Slate"),
        ("solar", "Bootswatch Solar"),
        ("spacelab", "Bootswatch Spacelab"),
        ("superhero", "Bootswatch Superhero"),
        ("united", "Bootswatch United"),
        ("yeti", "Bootswatch Yeti"),
    ]


# Helpers
# -------
def global_parameters(section, name):
    global_preferences = global_preferences_registry.manager()
    param = f"{section}__{name}" if section else name
    return global_preferences[param]
