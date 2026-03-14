class ProductRouter:

    def db_for_read(self, model, **hints):
        if model.__name__ == "Product":
            return "products"
        
        return "default"



    def db_for_write(self, model, **hints):
        if model.__name__ == "Product":
            return "products"
        
        return "default"


    def allow_relation(self, obj1, obj2, **hints):
        return True


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Product model should never be migrated (it's in MongoDB and managed=False)
        if model_name == "product":
            return False
        
        # ProductStore and ProductReview should only migrate on default (MySQL)
        if app_label == "products":
            return db == "default"
        
        # All other apps should only migrate on default
        return db == "default"
