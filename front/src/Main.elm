module Main exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick, onInput)
import Http
import Json.Decode exposing (Decoder, field, maybe, string)



-- MODEL


type Model
    = UserInput String
    | Success Username Repositories
    | Loading
    | Failure String


type alias Username =
    String


type alias Repositories =
    List Repository


type alias Repository =
    { name : String, language : String, description : Maybe String }


init : () -> ( Model, Cmd Msg )
init _ =
    ( UserInput ""
    , Cmd.none
    )



-- UPDATE


type Msg
    = GetRepositories Username Source
    | GotRepositories Username (Result Http.Error Repositories)
    | UpdateUserInput String


type Source
    = Database
    | Github


apiLink =
    "http://127.0.0.1:5000/api"


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GetRepositories username source ->
            case source of
                Database ->
                    ( Loading
                    , Http.get { url = apiLink ++ "/user/name/" ++ username, expect = Http.expectJson (GotRepositories username) repositoriesDecoder }
                    )

                Github ->
                    ( Loading
                    , Http.get { url = apiLink ++ "/scrape/" ++ username, expect = Http.expectJson (GotRepositories username) repositoriesDecoder }
                    )

        GotRepositories username result ->
            case result of
                Ok repositories ->
                    ( Success username repositories, Cmd.none )

                Err error ->
                    case error of
                        Http.BadUrl url ->
                            ( Failure url, Cmd.none )

                        Http.Timeout ->
                            ( Failure "timeout", Cmd.none )

                        Http.NetworkError ->
                            ( Failure "network error", Cmd.none )

                        Http.BadStatus status ->
                            ( Failure (String.fromInt status), Cmd.none )

                        Http.BadBody body ->
                            ( Failure body, Cmd.none )

        UpdateUserInput userInput ->
            ( UserInput userInput, Cmd.none )



-- HTTP


repositoryDecoder : Decoder Repository
repositoryDecoder =
    Json.Decode.map3 Repository (field "name" string) (field "lang" string) (field "description" <| maybe string)


repositoriesDecoder : Decoder Repositories
repositoriesDecoder =
    Json.Decode.list repositoryDecoder



-- VIEW


view : Model -> Html Msg
view model =
    div []
        [ viewHeader "Repo Scraper"
        , viewModel model
        , viewFooter
        ]


viewModel : Model -> Html Msg
viewModel model =
    case model of
        UserInput userInput ->
            viewUserInput userInput

        Success username repositories ->
            viewSuccess username repositories

        Loading ->
            main_ [] [ text "Repositories are loading..." ]

        Failure error ->
            main_ [] [ text <| "Error: " ++ error ]


viewUserInput userInput =
    main_ []
        [ text "Enter a username"
        , viewInput "text" "Username" userInput UpdateUserInput
        , button [ onClick (GetRepositories userInput Github) ] [ text "Scrape Repositories from Github" ]
        , button [ onClick (GetRepositories userInput Database) ] [ text "Check Repositories in the Database" ]
        ]


viewSuccess username repositories =
    main_ []
        [ h2 [] [ text <| "You are currently viewing repositories of " ++ username ]
        , ul []
            (List.map
                (\repo ->
                    li []
                        [ ul []
                            [ li [] [ text repo.name ]
                            , li [] [ text repo.language ]
                            ]
                        ]
                )
                repositories
            )
        ]


viewHeader : String -> Html msg
viewHeader title =
    header [] [ h1 [] [ text title ] ]


viewFooter : Html msg
viewFooter =
    footer [] [ text "This is a footer" ]


viewInput : String -> String -> String -> (String -> msg) -> Html msg
viewInput t p v toMsg =
    input [ type_ t, placeholder p, value v, onInput toMsg ] []



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- MAIN


main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }
