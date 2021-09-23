from amiibo import AmiiboMasterKey
import random
from ssbu_amiibo import SsbuAmiiboDump as AmiiboDump

SPIRITSKILLS = {
'none': 0,
'movespeedup': 1,
'hypersmashattacks': 2,
'jumpup': 4,
'additionalmidairjump': 5,
'easierdodging': 8,
'easierperfectshield': 9,
'superarmor': 10,
'slowsuperarmor': 11,
'trade-offattacksup': 12,
'trade-offdefenseup': 13,
'trade-offspeedup': 14,
'trade-offabilityup': 15,
'critical-healthattackup': 16,
'critical-healthdefenseup': 17,
'critical-healthstatsup': 18,
'criticalimmunity': 19,
'autoheal': 20,
'poisonimmunity': 21,
'poisondamagereduced': 22,
'poisonheals': 23,
'lava-floorimmunity': 24,
'sticky-floorimmunity': 25,
'beamswordequipped': 26,
'lipsstickequipped': 27,
'starrodequipped': 28,
'oreclubequipped': 29,
'raygunequipped': 31,
'superscopeequipped': 32,
'drillequipped': 34,
'greenshellequipped': 35,
'backshieldequipped': 38,
'bunnyhoodequipped': 39,
'madeofmetal': 40,
'mouthfulofcurry': 41,
'franklinbadgeequipped': 42,
'fairybottleequipped': 44,
'fireflowerequipped': 45,
'freezieequipped': 46,
'ramblinevilmushroomequipped': 47,
'killingedgeequipped': 48,
'physicalattackup': 50,
'weaponattackup': 51,
'fistattackup': 52,
'footattackup': 53,
'auraattackup': 54,
'magicattackup': 55,
'psiattackup': 56,
'fire&explosionattackup': 58,
'electricattackup': 60,
'energy-shotattackup': 61,
'water&iceattackup': 62,
'magicresistup': 63,
'psiresistup': 64,
'fire/explosionresistup': 66,
'electricresistup': 69,
'energy-shotresistup': 70,
'water/freezingresistup': 72,
'auraresistup': 73,
'zap-floorimmunity': 74,
'slumberimmunity': 75,
'ice-floorimmunity': 76,
'fallingimmunity': 77,
'buryimmunity': 78,
'brakingabilityup': 79,
'landinglagdown': 81,
'lightweight': 82,
'shielddamageup': 83,
'airattackup': 84,
'airdefenseup': 85,
'neutralspecialup': 86,
'sidespecialup': 87,
'upspecialup': 88,
'downspecialup': 89,
'strongthrow': 90,
'unflinchingchargedsmashes': 91,
'toss&meteor': 92,
'criticalhitup': 94,
'swimmer': 95,
'shielddurabilityup': 96,
'improvedescape': 97,
'batteringitemsup': 101,
'shootingitemsup': 102,
'thrownitemsup': 103,
'koshealdamage': 104,
'invincibilityaftereating': 105,
'statsupaftereating': 106,
'first-strikeadvantage': 108,
'runningstart': 110,
'fastfinalsmashmeter': 112,
'instadrop': 113,
'healingshield': 114,
'floatyjumps': 117,
'irreversiblecontrols': 119,
'transformationdurationup': 121,
'undamagedattackup': 122,
'undamagedspeedup': 123,
'undamagedattack&speedup': 124,
'impactrun': 128,
'lava-floorresist': 130,
'itemgravitation': 131,
'chanceofdoublefinalsmash': 133,
'doublefinalsmash': 134,
'giant': 138,
'dashattackup': 139,
'armorknight': 140,
'energyshotattack/resistanceup': 142,
'hammerdurationup': 143,
'boomerangequipped': 144,
'perfect-shieldreflect': 151,
'weaponattack&movespeedup': 152,
'shootingattackup': 153,
'screen-flipimmunity': 156,
'fogimmunity': 157,
'gravity-changeimmunity': 158,
'staminaup': 159,
'strong-windresist': 160,
'strong-windimmunity': 161,
'critical-healthhealing': 162,
'special-movepowerup': 163,
'bob-ombequipped': 165,
'hotheadequipped': 166,
'superleafequipped': 167,
'superlaunchstarequipped': 168,
'beastballequipped': 169,
'deathsscytheequipped': 170,
'mr.saturnequipped': 171,
'uniraequipped': 172,
'rocketbeltequipped': 173,
'blackholeequipped': 174,
'statsupupaftereating': 176,
'critical-healthstatsupup': 178,
'criticalhitupup': 179,
'greatautoheal': 180,
'steeldiverequipped': 181,
'bananagunequipped': 182,
'rageblasterequipped': 183,
'staffequipped': 184,
'firebarequipped': 185,
'screwattackequipped': 186,
'bomberequipped': 187,
'giantkiller': 213,
'metalkiller': 214,
'assistkiller': 215,
'jamfscharge': 216,
'weaponresistup': 217,
'itemautograb': 227,
'teampowerup': 228,
'poisonpowerup': 230,
'criticalfastfinalsmashmeterupup': 231,
'critical-healthhealingupup': 232,
'criticalsupergiant': 233,
'mouthfulofcurryupup': 234,
'finalsmashup': 235,
'criticalhealing&metal': 236,
}
SKILLSLOTS = {
'none': 0,
'movespeedup': 1,
'hypersmashattacks': 1,
'jumpup': 1,
'additionalmidairjump': 2,
'easierdodging': 1,
'easierperfectshield': 1,
'superarmor': 3,
'slowsuperarmor': 2,
'trade-offattacksup': 1,
'trade-offdefenseup': 1,
'trade-offspeedup': 1,
'trade-offabilityup': 1,
'critical-healthattackup': 1,
'critical-healthdefenseup': 1,
'critical-healthstatsup': 1,
'criticalimmunity': 2,
'autoheal': 2,
'poisonimmunity': 2,
'poisondamagereduced': 1,
'poisonheals': 3,
'lava-floorimmunity': 2,
'sticky-floorimmunity': 2,
'beamswordequipped': 1,
'lipsstickequipped': 1,
'starrodequipped': 1,
'oreclubequipped': 3,
'raygunequipped': 2,
'superscopeequipped': 2,
'drillequipped': 1,
'greenshellequipped': 1,
'backshieldequipped': 1,
'bunnyhoodequipped': 1,
'madeofmetal': 1,
'mouthfulofcurry': 2,
'franklinbadgeequipped': 2,
'fairybottleequipped': 1,
'fireflowerequipped': 1,
'freezieequipped': 1,
'ramblinevilmushroomequipped': 1,
'killingedgeequipped': 1,
'physicalattackup': 1,
'weaponattackup': 1,
'fistattackup': 1,
'footattackup': 1,
'auraattackup': 1,
'magicattackup': 1,
'psiattackup': 1,
'fire&explosionattackup': 1,
'electricattackup': 1,
'energy-shotattackup': 1,
'water&iceattackup': 1,
'magicresistup': 1,
'psiresistup': 1,
'fire/explosionresistup': 1,
'electricresistup': 1,
'energy-shotresistup': 1,
'water/freezingresistup': 1,
'auraresistup': 1,
'zap-floorimmunity': 2,
'slumberimmunity': 1,
'ice-floorimmunity': 2,
'fallingimmunity': 1,
'buryimmunity': 1,
'brakingabilityup': 1,
'landinglagdown': 1,
'lightweight': 1,
'shielddamageup': 1,
'airattackup': 1,
'airdefenseup': 1,
'neutralspecialup': 1,
'sidespecialup': 1,
'upspecialup': 1,
'downspecialup': 1,
'strongthrow': 1,
'unflinchingchargedsmashes': 2,
'toss&meteor': 1,
'criticalhitup': 1,
'swimmer': 1,
'shielddurabilityup': 1,
'improvedescape': 1,
'batteringitemsup': 1,
'shootingitemsup': 1,
'thrownitemsup': 1,
'koshealdamage': 2,
'invincibilityaftereating': 2,
'statsupaftereating': 1,
'first-strikeadvantage': 2,
'runningstart': 2,
'fastfinalsmashmeter': 2,
'instadrop': 2,
'healingshield': 2,
'floatyjumps': 1,
'irreversiblecontrols': 2,
'transformationdurationup': 1,
'undamagedattackup': 1,
'undamagedspeedup': 1,
'undamagedattack&speedup': 1,
'impactrun': 1,
'lava-floorresist': 1,
'itemgravitation': 1,
'chanceofdoublefinalsmash': 2,
'doublefinalsmash': 3,
'giant': 2,
'dashattackup': 1,
'armorknight': 2,
'energyshotattack/resistanceup': 2,
'hammerdurationup': 1,
'boomerangequipped': 1,
'perfect-shieldreflect': 1,
'weaponattack&movespeedup': 2,
'shootingattackup': 1,
'screen-flipimmunity': 2,
'fogimmunity': 2,
'gravity-changeimmunity': 2,
'staminaup': 1,
'strong-windresist': 1,
'strong-windimmunity': 2,
'critical-healthhealing': 2,
'special-movepowerup': 1,
'bob-ombequipped': 1,
'hotheadequipped': 2,
'superleafequipped': 1,
'superlaunchstarequipped': 1,
'beastballequipped': 1,
'deathsscytheequipped': 1,
'mr.saturnequipped': 1,
'uniraequipped': 1,
'rocketbeltequipped': 1,
'blackholeequipped': 2,
'statsupupaftereating': 2,
'critical-healthstatsupup': 2,
'criticalhitupup': 2,
'greatautoheal': 3,
'steeldiverequipped': 2,
'bananagunequipped': 1,
'rageblasterequipped': 1,
'staffequipped': 1,
'firebarequipped': 1,
'screwattackequipped': 2,
'bomberequipped': 1,
'giantkiller': 1,
'metalkiller': 1,
'assistkiller': 1,
'jamfscharge': 2,
'weaponresistup': 2,
'itemautograb': 1,
'teampowerup': 2,
'poisonpowerup': 3,
'criticalfastfinalsmashmeterupup': 3,
'critical-healthhealingupup': 3,
'criticalsupergiant': 3,
'mouthfulofcurryupup': 3,
'finalsmashup': 2,
'criticalhealing&metal': 2,
}


class BinManager:
    def __init__(self, char_dict, key_directory=r'c:/code/leaderbot/Brain_Transplant_Assets/key_retail.bin'):
        """
        This class manages bin files, does transplants and serial editing
        :param char_dict:
        """
        self.characters = char_dict
        self.key_directory = key_directory
        with open(self.key_directory, 'rb') as fp_j:
            self.master_keys = AmiiboMasterKey.from_combined_bin(
                fp_j.read())
    def __open_bin(self, bin_location):
        """
        Opens a bin and makes it 540 bytes if it wasn't

        :param bin_location: file location of bin you want to open
        :return: opened bin
        """
        bin_fp = open(bin_location, 'rb')

        bin_dump = bytes()
        for line in bin_fp:
            bin_dump += line
        bin_fp.close()

        if len(bin_dump) == 540:
            with open(bin_location, 'rb') as fp:
                dump = AmiiboDump(self.master_keys, fp.read())
                return dump
        elif 532 <= len(bin_dump) <= 572:
            while len(bin_dump) < 540:
                bin_dump += b'\x00'
            if len(bin_dump) > 540:
                bin_dump = bin_dump[:-(len(bin_dump) - 540)]
            b = open(bin_location, 'wb')
            b.write(bin_dump)
            b.close()

            with open(bin_location, 'rb') as fp:
                dump = AmiiboDump(self.master_keys, fp.read())
                return dump
        else:
            return None

    def update_char_dictionary(self, new_char_dict):
        """
        Updates character dictionary

        :param new_char_dict: dictionary to replace old one with
        :return: None
        """
        self.characters = new_char_dict

    def randomize_sn(self, dump=None, bin_location=None):
        """
        Randomizes the serial number of a given bin dump
        :param dump: Pyamiibo dump of a bin
        :return: None
        """
        if bin_location is not None:
            dump = self.__open_bin(bin_location)
        serial_number = "04"
        while len(serial_number) < 20:
            temp_sn = hex(random.randint(0, 255))
            # removes 0x prefix
            temp_sn = temp_sn[2:]
            # creates leading zero
            if len(temp_sn) == 1:
                temp_sn = '0' + temp_sn
            serial_number += ' ' + temp_sn
        # if unlocked, keep it unlocked, otherwise unlock and lock
        if not dump.is_locked:
            dump.uid_hex = serial_number
        else:
            dump.unlock()
            dump.uid_hex = serial_number
            dump.lock()
        if bin_location is not None:
            with open(bin_location, 'wb') as fp:
                fp.write(dump.data)

    def setspirits(self, bin_location, attack, defense, ability1, ability2, ability3, saveAs_location):
        # open keys
        directory1 = r'c:\\code\\leaderbot\\Brain_Transplant_Assets'
        hexatk = int(attack)
        hexdef = int(defense)
        hexability1 = int(SPIRITSKILLS[ability1.lower()])
        hexability2 = int(SPIRITSKILLS[ability2.lower()])
        hexability3 = int(SPIRITSKILLS[ability3.lower()])
        maxstats = 5000
        with open(bin_location, 'rb') as fp:
            dump = AmiiboDump(self.master_keys, fp.read())
        dump.unlock()
        
        slotsfilled = SKILLSLOTS[ability1.lower()] + SKILLSLOTS[ability2.lower()] + SKILLSLOTS[ability3.lower()]
        if slotsfilled == 1:
            maxstats = maxstats - 300
        if slotsfilled == 2:
            maxstats = maxstats - 500
        if slotsfilled == 3:
            maxstats = maxstats - 800
        print(hexatk + hexdef)
        print(maxstats)
        if hexatk + hexdef <= maxstats:
            dump.data[0x1A4:0x1A6] = hexatk.to_bytes(2, 'little')
            dump.data[0x1A6:0x1A8] = hexdef.to_bytes(2, 'little')
            dump.data[0x140:0x141] = hexability1.to_bytes(1, 'little')
            dump.data[0x141:0x142] = hexability2.to_bytes(1, 'little')
            dump.data[0x142:0x143] = hexability3.to_bytes(1, 'little')
            dump.lock()
            with open(saveAs_location, 'wb') as fp:
                fp.write(dump.data)
        else: 
            dump.lock()
            raise IndexError('Illegal Bin')
            
    def transplant(self, bin_location, character, saveAs_location, randomize_SN=False):
        """
        Takes a bin and replaces it's character ID with given character's ID

        :param bin_location: file location of bin to use
        :param character: Character from char_dict you want to transplant into
        :param randomize_SN: If the bin SN should be randomized or not
        :param saveAs_location: location to save new bin
        :return: Character it was transplanted into
        """

        dump = self.__open_bin(bin_location)

        if dump is None:
            return None

        if randomize_SN:
            self.randomize_sn(dump)
        hex_tag = self.characters[character]
        hex_tag = hex_tag[0] + hex_tag[1] + ' ' + hex_tag[2] + hex_tag[3] + ' ' + hex_tag[4] + hex_tag[5] + ' ' + \
                  hex_tag[6] + hex_tag[7] + ' ' + hex_tag[8] + hex_tag[9] + ' ' + hex_tag[10] + hex_tag[11] + ' ' + \
                  hex_tag[12] + hex_tag[13] + ' ' + hex_tag[14] + hex_tag[15]

        try:
            dump.unlock()
        except:
            input('''
            Opening {} has failed.
            Hit any button to close the program.'''.format(bin))
            exit()
        dump.data[84:92] = bytes.fromhex(hex_tag)
        dump.lock()
        with open(saveAs_location, 'wb') as fp:
            fp.write(dump.data)
        return character

    def serial_swapper(self, donor, receiver, saveAs_location):
        """
        Transfer the SN of the donor to the receiver, saves new bin at given location

        :param donor: bin to give SN
        :param receiver: bin to receive SN
        :param saveAs_location: location to save new bin
        :return: None
        """
        donor_dump = self.__open_bin(donor)
        receiver_dump = self.__open_bin(receiver)

        if donor_dump is None or receiver_dump is None:
            return None

        receiver_dump.unlock()
        # RO areas from https://wiki.gbatemp.net/wiki/Amiibo give FP metadata needed for transplant
        receiver_dump.data[0:17] = donor_dump.data[0:17]
        receiver_dump.data[52:129] = donor_dump.data[52:129]
        receiver_dump.data[520:533] = donor_dump.data[520:533]
        receiver_dump.lock()

        with open(saveAs_location, 'wb') as fp:
            fp.write(receiver_dump.data)

        return True
