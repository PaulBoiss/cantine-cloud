from app.app import app


def test_health():
    assert app.test_client().get("/health").get_json() == {"status": "ok"}


def test_accueil_donne_l_hote():
    corps = app.test_client().get("/").get_json()
    assert corps["app"] == "cantine"
    assert corps["host"]


def test_menus_du_lundi():
    corps = app.test_client().get("/menus?day=lundi").get_json()
    assert corps == [{"plat": "Lasagnes", "prix": 4.5}]


def test_jour_inconnu():
    assert app.test_client().get("/menus?day=samedi").status_code == 400
