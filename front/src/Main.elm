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
    | Success String Repositories
    | Loading
    | Failure String


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
    = GetRepositories String
    | GotRepositories String (Result Http.Error Repositories)
    | UpdateUserInput String


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GetRepositories username ->
            ( Loading, Http.get { url = "http://127.0.0.1:5000/api/scrape/" ++ username, expect = Http.expectJson (GotRepositories username) repositoriesDecoder } )

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
            main_ []
                [ text "Enter a username or link to the user"
                , viewInput "text" "Username" userInput UpdateUserInput
                , button [ onClick (GetRepositories userInput) ] [ text "Find Repositories" ]
                ]

        Success username repositories ->
            main_ []
                [ h2 [] [ text <| "You are currently viewing repositories of " ++ username ]
                , ul [] (List.map (\repo -> li [] [ ul [] [ li [] [ text repo.name ], li [] [ text repo.language ] ] ]) repositories)
                ]

        Loading ->
            main_ [] [ text "Repositories are loading..." ]

        Failure error ->
            main_ [] [ text error ]


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
