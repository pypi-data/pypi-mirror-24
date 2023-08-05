import {Component} from '@angular/core'
import {Type} from 'app/type.enum'
import {OptionFormComponent} from 'app/cls-form/fields/option-form.comp'
import {ComponentFactoryResolver} from '@angular/core'
import {ViewContainerRef} from '@angular/core'
import {ComponentRef, ViewChild} from '@angular/core'
import {TypeEnumDecorator} from 'app/type.enum.decorator'
import {OnInit, ViewEncapsulation} from '@angular/core'
import {Cls} from 'app/models/cls.model'
import {ClsNetworkService} from 'app/services/network/cls.service'
import {ProductType} from 'app/models/product-type.model'
import {ProductTypeNetworkService} from 'app/services/network/product-type.service'
import {NotifyService} from 'app/services/notify.service'
import {SlimLoadingBarService} from 'ng2-slim-loading-bar'
import {asyncShowLoadingBar} from 'app/services/decorators/loading-bar.serivce'
import {asyncNotifyOn} from 'app/services/decorators/notify.serivce'


@Component({
    selector: 'cls-form',
    moduleId: module.id,
    templateUrl: 'cls-form.comp.html',
    styleUrls: ['cls-form.comp.css'],
    encapsulation: ViewEncapsulation.None,
})
@TypeEnumDecorator
export class ClsFormComponent implements OnInit {
    // TODO make tha name field required
    model: Cls
    productTypeList: Array<ProductType>

    optionRefSet: Set<ComponentRef<OptionFormComponent>> = new Set()
    @ViewChild('options', {read: ViewContainerRef})
    private optionsContainerRef: ViewContainerRef

    constructor(
        private networkService: ClsNetworkService,
        private productTypeService: ProductTypeNetworkService,
        private notifyService: NotifyService,
        private loadingBarService: SlimLoadingBarService,
        private componentFactoryResolver: ComponentFactoryResolver,
    ) { }

    ngOnInit() {
        let clsStubForRender = new Cls({
            code: '',
            type: Type.INT,
            productType: {name: '', pk: 0},
        })
        this.model = clsStubForRender

        this.initForm()
    }

    setType(typeValueRaw: string) {
        let typeNew: Type = Number(typeValueRaw)
        this.model.type = typeNew
    }

    setProductType(productTypePkRaw: string) {
        let pkSelected: PrimaryKey = Number(productTypePkRaw)
        this.model.productType = this.productTypeList
            .find(productType => productType.pk === pkSelected) as ProductType
    }

    addOption(args?: {
        optionPk?: PrimaryKey | undefined,
        type?: Type | undefined,
        clsPk?: PrimaryKey | undefined,
    }) {
        let ref: ComponentRef<OptionFormComponent> = this.createOptionComponent()
        if (args) {
            ref.instance.initForm(args)
        } else {
            ref.instance.initForm({type: this.model.type, clsPk: this.model.pk})
        }
        this.optionRefSet.add(ref)
    }

    @asyncShowLoadingBar
    @asyncNotifyOn({success: 'The saving complete', error: 'The saving failed'})
    async save() {
        let clsSaved = await this.saveCls()
        await this.saveOptions(clsSaved.pk as PrimaryKey)
    }

    @asyncShowLoadingBar
    @asyncNotifyOn({success: null, error: 'Creation failed'})
    async create() {
        let clsCreated = await this.networkService.create(this.model)
        await this.saveOptions(clsCreated.pk as PrimaryKey)
        location.assign(`/sa/attrim/${clsCreated.pk}/`)
    }

    private async saveCls(): Promise<Cls> {
        let clsSaved: Cls = await this.networkService.save(this.model)
        this.model = clsSaved
        return clsSaved
    }

    private async saveOptions(clsPk: PrimaryKey) {
        let optionSavePromises: Array<Promise<any>> = []
        for (let optionRef of this.optionRefSet) {
            optionRef.instance.model.clsPk = clsPk
            let savePromise = optionRef.instance.save()
            optionSavePromises.push(savePromise)
        }
        await Promise.all(optionSavePromises)
    }

    @asyncShowLoadingBar
    private async initForm() {
        await this.initProductTypeList()
        if (window.DJANGO.isEditForm) {
            this.loadFormDataFromServer()
        } else {
            this.loadFormDataDefault()
        }
    }

    @asyncNotifyOn({success: null, error: 'Network error during product types retrieving'})
    private async initProductTypeList() {
        this.productTypeList = await this.productTypeService.getAll()
    }

    private async loadFormDataFromServer() {
        let clsPkToEdit = window.DJANGO.clsPrimaryKey as PrimaryKey
        let clsToEdit = await this.networkService.get(clsPkToEdit)
        this.model = clsToEdit

        for (let optionPk of clsToEdit.optionsPk) {
            this.addOption({optionPk: optionPk})
        }
    }

    private loadFormDataDefault() {
        let clsDefault = new Cls({
            code: '',
            type: Type.INT,
            productType: this.productTypeList[0],
        })
        this.model = clsDefault
    }

    private createOptionComponent(): ComponentRef<OptionFormComponent> {
        let factory = this.componentFactoryResolver
            .resolveComponentFactory(OptionFormComponent)
        return this.optionsContainerRef.createComponent(factory)
    }
}
