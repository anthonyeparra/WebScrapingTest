from Class.DataBase import DataBase
from Models.DBModels.CufesInformationModel import CufesInformation
ACTIVE = 1
INACTIVE = 0

class ProcessSQL:
    def create_informations_cufes(self,cufes, data: dict):
        """
        Creates a new CufesInformation object and adds it to the database.

        :param cufes: A string representing the cufes.
        :param data: A dictionary containing the extracted data.
        :type cufes: str
        :type data: dict
        :return: A CufesInformation object representing the newly created information.
        :rtype: CufesInformation
        """
        init_data = {"cufes": cufes, "extracted_data": data}
        with DataBase().session as db_write:
        # Obtener información de consorcios activos de una empresa
            cufes_informations = CufesInformation(
                init_data
            )
            db_write.add(cufes_informations)
            db_write.commit()
        return cufes_informations
        