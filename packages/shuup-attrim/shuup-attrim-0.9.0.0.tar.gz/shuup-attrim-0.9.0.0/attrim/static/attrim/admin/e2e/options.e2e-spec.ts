import {browser} from 'protractor'
import {$, $$} from 'protractor'
import FakerStatic = Faker.FakerStatic
import {loadClsEditForm} from './utils/navigation'
import {init} from './utils/init'


describe('options test', () => {
    beforeAll(async (done) => {
        await init()
        done()
    })

    beforeEach(async (done) => {
        await loadClsEditForm()
        done()
    })

    it('inits the options', () => {
        let optionValueInputEn = $$('option-form trans-str input[data-lang-code="en"]').first()
        let optionValueInputEnValue = optionValueInputEn.getAttribute('value')
        expect(optionValueInputEnValue).toBe('english')
    })

    it('edits the option value', async (done) => {
        let optionValueButtonFiSelector = `option-form trans-str .button[data-lang-code="fi"]`
        await $$(optionValueButtonFiSelector).first().click()
        let optionValueInputFiSelector = `option-form trans-str input[data-lang-code="fi"]`
        let optionValueInputFi = $(optionValueInputFiSelector)
        let optionValueInputFiNew = 'new fi option value'
        await optionValueInputFi.clear()
        await optionValueInputFi.sendKeys(optionValueInputFiNew)

        await $('#cls-save-button').click()
        await browser.waitForAngular()

        await loadClsEditForm()

        await $$(optionValueButtonFiSelector).first().click()
        let optionValueInputEnValue = await $(optionValueInputFiSelector).getAttribute('value')
        expect(optionValueInputEnValue).toBe(optionValueInputFiNew)

        done()
    })

    it('adds and deletes an option', async (done) => {
        // create a new option
        $('#add-option').click()
        let optionNewValue = 'some value'
        let optionInputSelector = `option-form trans-str input[data-lang-code="en"]`
        let optionNewInput = $$(optionInputSelector).last()
        await optionNewInput.sendKeys(optionNewValue)
        await $('#cls-save-button').click()
        await browser.waitForAngular()

        // check that the new option created
        await loadClsEditForm()
        let optionNewValueActual = await optionNewInput.getAttribute('value')
        expect(optionNewValueActual).toBe(optionNewValue)

        // remove the new option
        let optionNewRemoveInput = $$('option-form .option-remove input').last()
        await optionNewRemoveInput.click()
        await $('#cls-save-button').click()
        await browser.waitForAngular()

        // check that the new option was removed
        await loadClsEditForm()
        let optionLastInputValue = await $$(optionInputSelector).last()
            .getAttribute('value')
        expect(optionLastInputValue).not.toBe(optionNewValue)
        done()
    })
})
