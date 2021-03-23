from webmotors.scrap import Webmotors,IMAGE_URL
from models.models import *
import configparser
import logging
from time import sleep


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

confFile = configparser.ConfigParser()
confFile.read_file(open('config.ini'))

def saveVehicle(typeVehicle,vehicles):

    for v in vehicles:
        if session.query(Vehicle).filter_by(id=v["UniqueId"]).first():
            # Atualiza
            pass
        else:
            vehicle                 = Vehicle()
            vehicle.id              = int(v["UniqueId"])
            vehicle.typeVehicle     = typeVehicle
            try:
                vehicle.armored = False if v["Specification"]["Armored"] == 'N' else True
            except:
                vehicle.armored = None

            vehicle.title           = v["Specification"]["Title"]
            vehicle.yearFabrication = v["Specification"]["YearFabrication"]
            vehicle.yearModel       = v["Specification"]["YearModel"]
            vehicle.odometer        = v["Specification"]["Odometer"]

            try:
                vehicle.transmission    = v["Specification"]["Transmission"]
            except:
                vehicle.transmission = None

            try:
                vehicle.numberPorts = v["Specification"]["NumberPorts"]
            except:
                vehicle.numberPorts = None

            vehicle.bodyType        = v["Specification"]["BodyType"]
            vehicle.price           = v["Prices"]["Price"]
            vehicle.productCode     = v["ProductCode"]
            vehicle.listingType     = v["ListingType"]

            try:
                vehicle.fipePercent = float(v["FipePercent"])
            except:
                vehicle.fipePercent = None
                
            try:
                vehicle.comment = v["LongComment"]
            except:
                vehicle.comment = None

            try:
                for photo in v["Media"]["Photos"]:
                    photoPath = photo["PhotoPath"].replace("\\","/")
                    media = Media()
                    media.photoPath = photoPath
                    vehicle.medias.append(media)
            except:
                pass

            try:
                for att in v["Specification"]["VehicleAttributes"]:
                    attribute = Attribute()
                    attribute.name = att["Name"]
                    vehicle.attributes.append(attribute)
            except:
                pass
            
            seller = session.query(Seller).filter_by(id=v["Seller"]["Id"]).first()
            if not seller:
                seller                   = Seller()
                seller.id                = int(v["Seller"]["Id"])
                seller.sellerType        = v["Seller"]["SellerType"]
                seller.city              = v["Seller"]["City"]
                seller.state             = v["Seller"]["State"]
                seller.budgetInvestiment = v["Seller"]["BudgetInvestimento"]
                seller.dealerScore       = v["Seller"]["DealerScore"]
                seller.carDelivery       = v["Seller"]["CarDelivery"]
                seller.trocaComTroco     = v["Seller"]["TrocaComTroco"]
                seller.exceededPlan      = v["Seller"]["ExceededPlan"]
                session.add(seller)

            make = session.query(Make).filter_by(id=v["Specification"]["Make"]["id"]).first()
            if not make:
                make       = Make()
                make.id    = int(v["Specification"]["Make"]["id"])
                make.value = v["Specification"]["Make"]["Value"]
                session.add(make)

            if typeVehicle != 'moto':
                version = session.query(Version).filter_by(id=v["Specification"]["Version"]["id"]).first()
                if not version:
                    version       = Version()
                    version.id    = int(v["Specification"]["Version"]["id"])
                    version.value = v["Specification"]["Version"]["Value"]
                    session.add(version)

            model = session.query(Model).filter_by(id=v["Specification"]["Model"]["id"]).first()
            if not model:
                model       = Model()
                model.id    = int(v["Specification"]["Model"]["id"])
                model.value = v["Specification"]["Model"]["Value"]
                session.add(model)

            color = session.query(Color).filter_by(id=int(v["Specification"]["Color"]["IdPrimary"])).first()
            if not color:
                color         = Color()
                color.id      = int(v["Specification"]["Color"]["IdPrimary"])
                color.primary = v["Specification"]["Color"]["Primary"]
                session.add(color)
            
            logger.info(f"{vehicle.title}")

            vehicle.color_id   = color.id
            vehicle.model_id   = model.id
            vehicle.make_id    = make.id
            if typeVehicle != 'moto':
                vehicle.version_id = version.id
            else:
                vehicle.version_id = None
            vehicle.seller_id  = seller.id
            session.add(vehicle)
    session.commit()
    
def main():
    vehiclePerPage = int(confFile["WEBMOTORS"]["vehiclePerPage"])
    wait           = int(confFile["WEBMOTORS"]["waitForNext"])
    scrap          = Webmotors(vehiclePerPage=vehiclePerPage)
    while True:
        cars  = scrap.getCars()
        saveVehicle("carro",cars)
        bikes = scrap.getBikes()
        saveVehicle("moto",bikes)
        sleep(wait)

if __name__ == '__main__':
    main()