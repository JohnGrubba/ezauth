class Sos:
    saus: bool

    def validate(self):
        if type(self.saus) != bool:
            raise ValueError("Sausage must be a boolean")


Sos.saus = True
Sos().validate()
