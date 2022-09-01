export class ResponseItemsModel<Type> {
  constructor(
    public count: number,
    public last: string,
    public items:Type[]
  ) {}
}
