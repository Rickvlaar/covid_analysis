from database import data_model, engine


# Should only be run one time to build the schema
def create_data_model():
    data_model.Base.metadata.create_all(bind=engine)


# Drop all tables if you want to rebuild the data-model
def drop_all_tables(confirmed):
    if confirmed:
        data_model.Base.metadata.drop_all(bind=engine)
