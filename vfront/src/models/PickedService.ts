export class PickedService {
    constructor(
        public picked: boolean,

        public service_id: number,
        public name: string,
        public price: number,
        public seconds: number,
        public price_lower_bound?: number,
        public price_higher_bound?: number,
        public description?: string, 
    ){}
}