export class ShortUserResponseModel {
  constructor(
    public username: string,
    public firstname: string,
    public lastname: string,
    public key?: string,
    public url?: string
  ) {}
}
